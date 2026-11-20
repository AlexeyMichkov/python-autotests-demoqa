import allure
import pytest
from pages.forms_page import FormsPage


@allure.epic("DemoQA")
@allure.feature("Forms")
@pytest.mark.ui
@pytest.mark.smoke
class TestForms:

    @allure.story("Успешная отправка формы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_form_success(self, page):
        """Тест: заполнение формы и проверка модального окна успеха."""
        forms_page = FormsPage(page)
        forms_page.open_forms()

        # Заполняем форму
        forms_page.fill_form(
            first_name="Alexey",
            last_name="Michkov",
            email="alexey@test.com"
        )

        # Отправляем форму
        forms_page.click_submit()

        # Проверяем, что появилось модальное окно успеха
        assert forms_page.is_success_modal_visible(), "Модальное окно успеха не появилось"

        # Закрываем модальное окно
        forms_page.close_modal()

    @allure.story("Валидация обязательных полей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_empty_form(self, page):
        """Тест: отправка пустой формы должна показать валидацию."""
        forms_page = FormsPage(page)
        forms_page.open_forms()

        # Пытаемся отправить пустую форму
        forms_page.click_submit()

        # Проверяем, что форма не отправилась (модальное окно не появилось)
        assert not forms_page.is_success_modal_visible(), "Форма отправилась, хотя должна была показать валидацию"