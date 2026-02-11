import pytest
import yaml  # Python 3.11+
from playwright.sync_api import sync_playwright
from utils.config_reader import ConfigReader

config=ConfigReader()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


# -------------------------
# Read browsers from TOML
# -------------------------
def pytest_addoption(parser):
    parser.addoption("--ui-browser", action="store", default=None)


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:

        cli_browser = metafunc.config.getoption("--ui-browser")

        if cli_browser:
            browser_list = [b.strip() for b in cli_browser.split(",")]
        else:
            browser_list = config.get("tool", "pytest", "ini_options", "browsers")

        metafunc.parametrize("browser", browser_list, indirect=True)

@pytest.fixture(scope="function")
def browser(playwright_instance, request):
    browser_name = request.param  # ✅ FIXED

    is_ci = os.getenv("CI", "false").lower() == "true"

    if is_ci:
        headless = True
    else:
        headless = config.get("tool", "pytest", "ini_options", "headless")

    browser = getattr(playwright_instance, browser_name).launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto(config.get("app_ui", "base_url"))

    yield page

    context.close()

import os

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=f"screenshots/{item.name}.png")

