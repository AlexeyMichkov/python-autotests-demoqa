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

    @allure.story("Заполнение всех полей и отправка")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_full_form(self, page):
        """Тест: заполнить ВСЕ поля (имя, фамилия, email, gender male, mobile,
        предмет "English", DOB, адрес), submit — модалка успеха с введёнными данными."""
        forms_page = FormsPage(page)
        with allure.step("Открыть форму"):
            forms_page.open_forms()

        with allure.step("Заполнить все поля формы"):
            forms_page.fill_first_name("Alexey")
            forms_page.fill_last_name("Michkov")
            forms_page.fill_email("alexey@test.com")
            forms_page.select_gender_male()
            forms_page.fill_mobile("9876543210")
            forms_page.select_subject("English")
            forms_page.fill_dob("01 January 1990")
            forms_page.fill_address("Ostankino, Moscow")

        with allure.step("Отправить форму"):
            forms_page.click_submit()

        with allure.step("Проверить модалку успеха и введённые данные"):
            assert forms_page.is_success_modal_visible(), "Модальное окно успеха не появилось"
            modal_text = forms_page.get_modal_content()
            assert "Alexey Michkov" in modal_text, "Имя не отображается в модалке"
            assert "alexey@test.com" in modal_text, "Email не отображается в модалке"
            assert "Male" in modal_text, "Пол Male не отображается в модалке"
            assert "9876543210" in modal_text, "Мобильный не отображается в модалке"
            assert "English" in modal_text, "Предмет English не отображается в модалке"
            assert "Ostankino, Moscow" in modal_text, "Адрес не отображается в модалке"
            forms_page.close_modal()

    @allure.story("Валидация email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_email_validation(self, page):
        """Тест: email 'abc' — submit не ведёт к модалке успеха (валидация блокирует отправку)."""
        forms_page = FormsPage(page)
        with allure.step("Открыть форму"):
            forms_page.open_forms()

        with allure.step("Заполнить имя, фамилию и email 'abc'"):
            forms_page.fill_first_name("Alexey")
            forms_page.fill_last_name("Michkov")
            forms_page.fill_email("abc")

        with allure.step("Отправить форму"):
            forms_page.click_submit()

        with allure.step("Проверить: модалка успеха не появилась, email остался в поле"):
            assert not forms_page.is_success_modal_visible(), "Модалка успеха появилась с невалидным email"
            assert page.locator(FormsPage.EMAIL_INPUT).input_value() == "abc"

    @allure.story("Валидация пустой формы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_empty_form_validation(self, page):
        """Тест: пустая форма — submit не ведёт к модалке успеха, отправка заблокирована."""
        forms_page = FormsPage(page)
        with allure.step("Открыть форму"):
            forms_page.open_forms()

        with allure.step("Отправить пустую форму"):
            forms_page.click_submit()

        with allure.step("Проверить: модалка успеха не появилась, поля формы на месте"):
            assert not forms_page.is_success_modal_visible(), "Модалка успеха появилась для пустой формы"
            assert page.locator(FormsPage.FIRST_NAME_INPUT).is_visible()
            assert page.locator(FormsPage.LAST_NAME_INPUT).is_visible()
            assert page.locator(FormsPage.EMAIL_INPUT).is_visible()