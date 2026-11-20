import allure
from playwright.sync_api import Page


class BasePage:
    """Базовый класс для Page Objects."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открыть страницу: {path}")
    def open(self, path: str):
        self.page.goto(path, wait_until="domcontentloaded")

    @allure.step("Кликнуть по элементу: {selector}")
    def click(self, selector: str):
        self.page.locator(selector).click()

    @allure.step("Получить текст элемента: {selector}")
    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()