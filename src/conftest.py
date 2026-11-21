import allure
import httpx
import pytest
from playwright.sync_api import Page, BrowserContext

from config import config


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


@pytest.fixture()
def context(browser) -> BrowserContext:
    ctx = browser.new_context(base_url=config.BASE_URL)
    yield ctx
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture()
def api_client() -> httpx.Client:
    """HTTP-клиент для API-тестов. Базовый URL — config.BOOKSTORE_URL."""
    with httpx.Client(base_url=config.BOOKSTORE_URL, timeout=30) as client:
        yield client


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page and not page.is_closed():
            with allure.step("Прикрепить скриншот падения"):
                allure.attach(
                    page.screenshot(full_page=True),
                    name="Скриншот падения",
                    attachment_type=allure.attachment_type.PNG,
                )


@pytest.fixture(autouse=True)
def allure_meta(request):
    allure.dynamic.link(config.BASE_URL, name="Демо-сайт")
    module = request.node.module.__name__
    allure.dynamic.feature(module.split(".")[-1])