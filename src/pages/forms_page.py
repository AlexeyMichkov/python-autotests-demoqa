import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class FormsPage(BasePage):
    """Page Object для страницы /forms на demoqa.com."""

    PATH = "/forms"

    FIRST_NAME_INPUT = "input#firstName"
    LAST_NAME_INPUT = "input#lastName"
    EMAIL_INPUT = "input#userEmail"
    GENDER_RADIO_MALE = "label[for='gender-radio-1']"
    MOBILE_INPUT = "input#userNumber"
    DOB_INPUT = "#dateOfBirthInput"
    SUBJECTS_INPUT = "#subjectsInput"
    SUBJECT_OPTION = '[role="option"]'  # устойчиво к номеру react-select
    SUBMIT_BUTTON = "button#submit"
    ADDRESS_INPUT = "textarea#currentAddress"
    SUCCESS_MODAL = "div.modal-content"
    CLOSE_MODAL_BUTTON = "button#closeLargeModal"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Открыть Forms и выбрать Practice Form")
    def open_forms(self):
        self.open(self.PATH)
        self.page.get_by_text("Practice Form").click()
        expect(self.page.locator(self.FIRST_NAME_INPUT)).to_be_visible(timeout=10000)

    @allure.step("Заполнить имя: {first_name}")
    def fill_first_name(self, first_name: str):
        self.page.fill(self.FIRST_NAME_INPUT, first_name)

    @allure.step("Заполнить фамилию: {last_name}")
    def fill_last_name(self, last_name: str):
        self.page.fill(self.LAST_NAME_INPUT, last_name)

    @allure.step("Заполнить email: {email}")
    def fill_email(self, email: str):
        self.page.fill(self.EMAIL_INPUT, email)

    @allure.step("Выбрать пол: Male")
    def select_gender_male(self):
        self.page.locator(self.GENDER_RADIO_MALE).click()

    @allure.step("Заполнить мобильный: {mobile}")
    def fill_mobile(self, mobile: str):
        self.page.fill(self.MOBILE_INPUT, mobile)

    @allure.step("Выбрать предмет: {subject}")
    def select_subject(self, subject: str):
        # react-select: клик по combobox -> ввод поиска -> клик по отфильтрованной опции
        self.page.click(self.SUBJECTS_INPUT)
        self.page.fill(self.SUBJECTS_INPUT, subject)
        self.page.locator(self.SUBJECT_OPTION).first.click()

    @allure.step("Выбрать дату рождения: {dob}")
    def fill_dob(self, dob: str):
        # ХРУПКОЕ МЕСТО: react-datepicker. fill+Enter — основной путь.
        # Если datepicker не примет ручной ввод — см. примечание ниже, переключимся на клик по календарю.
        self.page.click(self.DOB_INPUT)
        self.page.fill(self.DOB_INPUT, dob)
        self.page.keyboard.press("Enter")

    @allure.step("Заполнить адрес: {address}")
    def fill_address(self, address: str):
        self.page.fill(self.ADDRESS_INPUT, address)

    @allure.step("Нажать Submit")
    def click_submit(self):
        self.page.locator(self.SUBMIT_BUTTON).click()

    @allure.step("Проверить появление модального окна успеха")
    def is_success_modal_visible(self) -> bool:
        return self.page.locator(self.SUCCESS_MODAL).is_visible()

    @allure.step("Получить текст модального окна")
    def get_modal_content(self) -> str:
        return self.page.locator(self.SUCCESS_MODAL).inner_text()

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.page.locator(self.CLOSE_MODAL_BUTTON).click()

    @allure.step("Заполнить форму полностью")
    def fill_form(self, first_name: str, last_name: str, email: str):
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.select_gender_male()
        self.fill_mobile("9876543210")
        self.select_subject("Math")
        self.fill_dob("01 January 1990")