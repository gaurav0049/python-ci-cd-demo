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

pytest.fixture(scope="session")
def browser(playwright_instance, request):

    cli_browser = request.config.getoption("--ui-browser")

    # If CLI browser provided → use it
    if cli_browser:
        browser_name = cli_browser
    else:
        # Otherwise fallback to TOML config
        browser_name = config.get("tool", "pytest", "ini_options", "browsers")

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

