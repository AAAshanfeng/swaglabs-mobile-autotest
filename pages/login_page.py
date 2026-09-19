from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):

    username_input = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    password_input = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    login_btn = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    error_message = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Error '
                                     'message"]/android.widget.TextView')

    product_page_indicator = (AppiumBy.XPATH, "//android.widget.TextView[@text='PRODUCTS']")

    def input_username(self, username):
        self.wait.until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)

    def input_password(self, password):
        self.wait.until(
            EC.visibility_of_element_located(self.password_input)
        ).send_keys(password)

    def click_login_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.login_btn)
        ).click()

    def is_on_product_page(self):
        elements = self.wait.until(
            EC.visibility_of_all_elements_located(self.product_page_indicator)
        )

        return len(elements) > 0

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.error_message)
        ).text

    def is_on_login_page(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.login_btn)
            )
            return True
        except:
            return False

    def login(self, username, password):
        self.wait.until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_btn).click()