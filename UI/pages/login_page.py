from UI.Base_page.base_page import BasePage
from UI.locators.login_locators import LoginLocators


class LoginPage(BasePage):

    def login(self, username, password):
        self.fill(LoginLocators.USERNAME, username)
        self.fill(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BTN)

    def get_success_message(self):
        return self.get_text(LoginLocators.SUCCESS_MSG)
