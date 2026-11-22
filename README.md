# Python Autotests DemoQA

[![Tests](https://github.com/AlexeyMichkov/python-autotests-demoqa/actions/workflows/tests.yml/badge.svg)](https://github.com/AlexeyMichkov/python-autotests-demoqa/actions/workflows/tests.yml)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-UI-green)
![pytest](https://img.shields.io/badge/pytest-9-yellow)

---

## 📌 О проекте

Фреймворк для UI и API автотестов на [DemoQA](https://demoqa.com) и BookStore API — построен на **Page Object Model**, **Playwright**, **pytest** и **Allure**. CI/CD через GitHub Actions: параллельный запуск UI и API тестов, сбор суммарного покрытия кода и загрузка отчётов.

## 📂 Структура проекта

```
src/
├── pages/                  # Page Objects
│   ├── base_page.py        # Базовый класс Page Object (open, click, get_text)
│   ├── forms_page.py       # Page Object для страницы /forms (заполнение полей, модалки)
│   └── __init__.py
├── tests/                  # Тесты
│   ├── api/                # API-тесты (ToolsQA BookStore API)
│   │   ├── test_book_store.py
│   │   └── __init__.py
│   ├── ui/                 # UI-тесты (Playwright)
│   │   ├── test_forms.py
│   │   └── __init__.py
│   └── __init__.py
├── config.py               # Конфигурация (BASE_URL, BOOKSTORE_URL, API_USER, API_PASS)
└── conftest.py             # Фикстуры (api_client, context, page, delay_between_tests)
```

## 🛠 Технологии

- **Python 3.11+**
- **pytest** + pytest-xdist + pytest-cov + pytest-playwright
- **Playwright** — UI-тесты (Chromium)
- **httpx** + **pydantic** — API-тесты
- **Allure** — красивые отчёты
- **GitHub Actions** — CI/CD

## 🚀 Быстрый старт

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/AlexeyMichkov/python-autotests-demoqa.git
   cd python-autotests-demoqa
   ```

2. Создать и активировать виртуальное окружение:
   ```bash
   python -m venv .venv
   ```
   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`

3. Установить зависимости:
   ```bash
   pip install -e ".[dev]"
   ```

4. Установить браузеры:
   ```bash
   playwright install chromium
   ```

5. Создать файл `.env` (пример):
   ```ini
   BASE_URL=https://demoqa.com
   BOOKSTORE_URL=https://bookstore.toolsqa.com
   API_USER=ваш_пользователь
   API_PASS=ваш_пароль
   ```

6. Запустить тесты:
   ```bash
   # UI-тесты
   pytest src/tests/ui -v

   # API-тесты
   pytest src/tests/api -v

   # Все тесты с отчётом о покрытии
   pytest src/tests/ -n auto --cov=src --cov-report=html -v
   ```

## ⚙️ CI/CD

В GitHub Actions (`tests.yml`):
- Запуск при `push` и `pull_request` в ветку `main`
- Параллельный запуск (`-n auto`) UI и API тестов
- Сбор суммарного покрытия (`--cov=src --cov-append`) с проверкой `fail-under=90`
- Загрузка артефактов (`coverage-and-allure`: `allure-results/` + `htmlcov/`)

## 📊 Allure-отчёты

Отчёты генерируются автоматически (`--alluredir=allure-results`). Открыть локально:

```bash
allure serve allure-results/
```

## 📋 Список тестов

| Тест | Что проверяет |
|------|---------------|
| **UI: test_submit_form_success** | Заполнение формы — появление модалки успеха |
| **UI: test_submit_empty_form** | Отправка пустой формы — модалка успеха не появляется |
| **UI: test_submit_full_form** | Заполнение всех полей (имя, фамилия, email, пол, мобильный, предмет, DOB, адрес) — модалка успеха с введёнными данными |
| **UI: test_email_validation** | Невалидный email — отправка заблокирована |
| **UI: test_submit_empty_form_validation** | Пустая форма — отправка заблокирована |
| **API: test_get_all_books** | GET /BookStore/v1/Books — 200, ответ — список книг |
| **API: test_get_book_by_isbn** | GET /BookStore/v1/Book?ISBN= — структура книги (isbn, title, author) |
| **API: test_create_user** | POST /Account/v1/User — 201, возвращён userID |
| **API: test_add_book_to_collection** | POST /BookStore/v1/Books (Bearer) — книга добавлена в коллекцию |
| **API: test_delete_user** | DELETE /Account/v1/User/{userId} (Bearer) — пользователь удалён |
| **API: test_delete_collection_of_books** | DELETE /BookStore/v1/Books?UserId= (Bearer) — коллекция очищена |

## 📄 Лицензия

MIT
