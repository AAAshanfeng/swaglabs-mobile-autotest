from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage(BasePage):

    first_name = (AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    last_name = (AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    zip_code = (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code")
    cancel_btn = (AppiumBy.ACCESSIBILITY_ID, "test-CANCEL")
    continue_btn = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE")
    error_message = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")

    item_name = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Description"]/android.widget.TextView[1]')
    item_desc = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Description"]/android.widget.TextView[2]')
    item_price = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Price"]/android.widget.TextView')

    item_total = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Item total: $')]")
    tax = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Tax: $')]")
    total = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Total: $')]")

    finish_btn = (AppiumBy.ACCESSIBILITY_ID, "test-FINISH")
    complete_title = (AppiumBy.XPATH, '//android.widget.TextView[@text="CHECKOUT: COMPLETE!"]')
    back_home_btn = (AppiumBy.ACCESSIBILITY_ID, "test-BACK HOME")

    def input_firstname(self, firstname):
        self.wait.until(
            EC.visibility_of_element_located(self.first_name)
        ).send_keys(firstname)

    def input_lastname(self, lastname):
        self.wait.until(
            EC.visibility_of_element_located(self.last_name)
        ).send_keys(lastname)

    def input_zip(self, zipcode):
        self.wait.until(
            EC.visibility_of_element_located(self.zip_code)
        ).send_keys(zipcode)

    def click_cancel_btn(self):
        self.driver.find_element(*self.cancel_btn).click()

    def click_continue_btn(self):
        self.driver.find_element(*self.continue_btn).click()

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except:
            return None

    def fill_checkout_info(self, firstname, lastname, zipcode):
        self.input_firstname(firstname)
        self.input_lastname(lastname)
        self.input_zip(zipcode)

    # 详情
    def get_item_name(self):
        return self.driver.find_element(*self.item_name).text

    def get_item_desc(self):
        return self.driver.find_element(*self.item_desc).text

    def get_item_price(self):
        return self.driver.find_element(*self.item_price).text

    # 价格
    def get_item_total(self):
        text = self.driver.find_element(*self.item_total).text
        return float(text.split("$")[1])

    def get_tax(self):
        text = self.driver.find_element(*self.tax).text
        return float(text.split("$")[1])

    def get_total(self):
        text = self.driver.find_element(*self.total).text
        return float(text.split("$")[1])

    def click_finish_btn(self):
        self.driver.find_element(*self.finish_btn).click()

    def is_complete_page(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.complete_title)
            )
            return True
        except:
            return False

    def click_back_home_btn(self):
        self.driver.find_element(*self.back_home_btn).click()