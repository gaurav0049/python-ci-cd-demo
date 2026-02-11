import pytest
from UI.pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.login("admin", "admin123")
