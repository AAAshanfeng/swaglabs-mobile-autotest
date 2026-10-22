from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from utils.device_actions import DeviceActions


class CartPage(BasePage, DeviceActions):
    cart_title = (AppiumBy.XPATH, "//android.widget.TextView[@text='YOUR CART']")
    cart_item = (AppiumBy.ACCESSIBILITY_ID, "test-Item")
    product_name = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Description"]''/android.widget'
                                    '.TextView[1]')
    product_price = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Price"]//android.widget.TextView')
    remove_btn = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")
    continue_shopping_btn = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE SHOPPING")
    checkout_btn = (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT")

    def wait_for_cart_page_loaded(self):
        self.wait.until(
            EC.visibility_of_element_located(self.cart_title)
        )

    def is_on_cart_page(self):
        elements = self.wait.until(
            EC.visibility_of_all_elements_located(self.cart_title)
        )
        return len(elements) > 0

    def get_all_cart_item(self):
        return self.driver.find_elements(*self.cart_item)

    def get_all_cart_name(self):
        return self.driver.find_elements(*self.product_name)

    def click_continue_shopping(self):
        self.wait.until(
            EC.element_to_be_clickable(self.continue_shopping_btn)
        ).click()

    def click_checkout(self):
        self.driver.find_element(*self.checkout_btn).click()

    def get_first_cart_item_name(self):
        """获取购物车第一个商品的名称"""
        names = self.get_all_cart_name()
        if names:
            return names[0].get_attribute("text")
        raise Exception("购物车为空")

    def get_first_cart_item_price(self):
        """获取购物车第一个商品的价格"""
        prices = self.driver.find_elements(*self.product_price)
        if prices:
            return prices[0].get_attribute("text")
        raise Exception("购物车里没有价格信息")

    # def remove_first_product(self):
    #     """删除购物车里第一个商品"""
    #     self.driver.find_elements(*self.remove_btn)[0].click()
    #     # self.wait.until(
    #     #     EC.element_to_be_clickable(self.remove_btn)
    #     # ).click()
    def remove_first_product(self):
        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": 0,
                "top": 500,
                "width": 1080,
                "height": 1500,
                "direction": "down",
                "percent": 0.5
            }
        )
        btn = self.wait.until(
            lambda d: next(
                (element for element in d.find_elements(*self.remove_btn)
                 if element.is_displayed()),
                False
            )
        )
        btn.click()

    def is_cart_empty(self):
        """判断购物车是否为空"""
        items = self.get_all_cart_item()
        return len(items) == 0

    def get_all_items_count(self):
        """获得购物车页面的商品数量"""
        count = len(self.get_all_cart_item())
        return count