from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


class ProductDetailPage(BasePage):
    back_btn = (AppiumBy.ACCESSIBILITY_ID, "test-BACK TO PRODUCTS")
    add_to_cart_btn = (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    remove_btn = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")

    detail_image = (AppiumBy.ACCESSIBILITY_ID, "test-Image Container")
    detail_desc = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Description"]'
                                   '/android.widget.TextView[2]')
    detail_price = (AppiumBy.ACCESSIBILITY_ID, "test-Price")

    def get_detail_image(self):
        return self.driver.find_element(*self.detail_image)

    def get_detail_desc(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.detail_desc)
        )
        return element.text

    def get_detail_price(self):
        return self.driver.find_element(*self.detail_price).text

    def click_add_btn(self):
        self.driver.find_element(*self.add_to_cart_btn).click()

    def click_remove_btn(self):
        self.driver.find_element(*self.remove_btn).click()

    def click_back(self):
        self.driver.find_element(*self.back_btn).click()

    def is_add_to_cart(self):
        try:
            self.driver.find_element(*self.remove_btn)
            return True
        except:
            return False
