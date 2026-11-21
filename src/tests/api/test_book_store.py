"""API-тесты BookStore (https://bookstore.toolsqa.com)."""

import uuid

import httpx
import pytest

# Тестовые данные (hardcode)
ISBN = "9781449325862"  # ISBN из каталога: GET /BookStore/v1/Books
PASSWORD = "AutoTest#1234"


def _create_user(api_client):
    """Создаёт тестового пользователя. Возвращает (user_id, user_name)."""
    user_name = f"autotest_{uuid.uuid4().hex[:8]}"
    response = api_client.post(
        "/Account/v1/User",
        json={"userName": user_name, "password": PASSWORD},
    )
    assert response.status_code == 201, response.text
    return response.json()["userID"], user_name


def _generate_token(api_client, user_name):
    """Получает Bearer-токен по userName/password."""
    response = api_client.post(
        "/Account/v1/GenerateToken",
        json={"userName": user_name, "password": PASSWORD},
    )
    assert response.status_code == 200, response.text
    return response.json()["token"]


def _get_collection_isbns(api_client, user_id, token):
    """ISBN-ки из коллекции пользователя (GET /Account/v1/User/{userId})."""
    response = api_client.get(
        f"/Account/v1/User/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    return [book["isbn"] for book in response.json()["books"]]


@pytest.fixture()
def auth(api_client):
    """Создаёт пользователя (uuid-имя) и возвращает (userId, token)."""
    user_id, user_name = _create_user(api_client)
    token = _generate_token(api_client, user_name)
    return user_id, token


@pytest.mark.api
def test_get_all_books(api_client):
    """GET /BookStore/v1/Books — 200, ответ — список книг."""
    response = api_client.get("/BookStore/v1/Books")
    assert response.status_code == 200
    books = response.json()["books"]
    assert isinstance(books, list)


@pytest.mark.api
def test_get_book_by_isbn(api_client):
    """GET /BookStore/v1/Book?ISBN={isbn} — 200, структура ответа."""
    response = api_client.get("/BookStore/v1/Book", params={"ISBN": ISBN})
    assert response.status_code == 200
    book = response.json()
    assert book["isbn"] == ISBN
    assert book["title"]
    assert book["author"]


@pytest.mark.api
def test_create_user(api_client):
    """POST /Account/v1/User — 201, возвращён userID."""
    user_id, _ = _create_user(api_client)
    assert user_id


@pytest.mark.api
def test_add_book_to_collection(api_client, auth):
    """POST /BookStore/v1/Books — Bearer-токен, книга добавлена в коллекцию."""
    user_id, token = auth

    def _add():
        return api_client.post(
            "/BookStore/v1/Books",
            headers={"Authorization": f"Bearer {token}"},
            json={"userId": user_id, "collectionOfIsbns": [{"isbn": ISBN}]},
        )

    # retry + TimeoutException: ToolsQA-API иногда долго не отвечает
    response = None
    for _ in range(3):
        try:
            response = _add()
        except httpx.TimeoutException:
            response = None
            continue
        if response.status_code < 500:
            break
    assert response is not None and response.status_code == 201, response

    # Проверка: книга в коллекции (GET /Account/v1/User/{userId} -> books)
    assert ISBN in _get_collection_isbns(api_client, user_id, token)


@pytest.mark.api
def test_delete_user(api_client):
    """DELETE /Account/v1/User/{userId} — Bearer-токен, пользователь удалён."""
    user_id, user_name = _create_user(api_client)
    token = _generate_token(api_client, user_name)
    response = api_client.delete(
        f"/Account/v1/User/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204


@pytest.mark.api
def test_delete_collection_of_books(api_client, auth):
    """DELETE /BookStore/v1/Books — Bearer-токен + ?UserId=, коллекция очищена.

    ToolsQA не поддерживает удаление одной книги — DELETE с UserId
    очищает всю коллекцию, поэтому книгу сначала добавляем, а потом удаляем.
    """
    user_id, token = auth

    # сначала добавим книгу в коллекцию, чтобы затем её удалить
    add = api_client.post(
        "/BookStore/v1/Books",
        headers={"Authorization": f"Bearer {token}"},
        json={"userId": user_id, "collectionOfIsbns": [{"isbn": ISBN}]},
    )
    assert add.status_code == 201, add.text
    assert ISBN in _get_collection_isbns(api_client, user_id, token)

    # retry + TimeoutException: ToolsQA-API иногда долго не отвечает
    response = None
    for _ in range(3):
        try:
            response = api_client.request(
                "DELETE",
                "/BookStore/v1/Books",
                params={"UserId": user_id},
                headers={"Authorization": f"Bearer {token}"},
            )
        except httpx.TimeoutException:
            response = None
            continue
        if response.status_code == 204:
            break
        if response.status_code >= 500:
            continue
    assert response is not None and response.status_code == 204, response
    assert ISBN not in _get_collection_isbns(api_client, user_id, token)
