from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from utils.device_actions import DeviceActions
import time
from selenium.common.exceptions import StaleElementReferenceException


class ProductPage(BasePage, DeviceActions):

    title = (AppiumBy.XPATH, "//android.widget.TextView[@text='PRODUCTS']")
    menu_btn = (AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    cart_btn = (AppiumBy.ACCESSIBILITY_ID, "test-Cart")
    cart_count = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Cart"]''//android.widget.TextView')

    sort_btn = (AppiumBy.ACCESSIBILITY_ID, "test-Modal Selector Button")
    sort_name_up = (AppiumBy.XPATH, "//android.widget.TextView[@text='Name (A to Z)']")
    sort_price_up = (AppiumBy.XPATH, "//android.widget.TextView[@text='Price (low to high)']")

    add_to_cart_btn = (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    remove_btn = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")
    first_product_detail = (AppiumBy.XPATH, "(//android.view.ViewGroup[@content-desc='test-Item'])[1]")

    product_name = (AppiumBy.ACCESSIBILITY_ID, "test-Item title")
    product_price = (AppiumBy.ACCESSIBILITY_ID, "test-Price")
    product_image = (AppiumBy.XPATH,
                     "//android.widget.ScrollView[@content-desc='test-PRODUCTS']"
                     "//android.widget.ImageView")

    def open_menu(self):
        self.wait.until(
            EC.element_to_be_clickable(self.menu_btn)
        ).click()

    def open_cart(self):
        for attempt in range(3):
            try:
                self.wait.until(
                    EC.element_to_be_clickable(self.cart_btn)
                ).click()
                return
            except StaleElementReferenceException:
                time.sleep(0.5)
        # 三次都失败，最后再试一次，让它自然抛出真实异常
        self.wait.until(EC.element_to_be_clickable(self.cart_btn)).click()

    def click_sort_dropdown(self):
        self.driver.find_element(*self.sort_btn).click()

    # 排序
    def click_sort_by_name(self):
        self.driver.find_element(*self.sort_name_up).click()

    def click_sort_by_price(self):
        self.driver.find_element(*self.sort_price_up).click()

    # 按键
    def get_all_add_to_car_btn(self):
        """得到所有添加键列表"""
        return self.driver.find_elements(*self.add_to_cart_btn)

    def get_all_remove_btn(self):
        """得到所有删除键列表"""
        return self.driver.find_elements(*self.remove_btn)

    # 商品
    def get_all_product_title(self):
        """得到所有商品名称列表"""
        return self.driver.find_elements(*self.product_name)

    def get_all_product_price(self):
        """获得所有商品的价格列表"""
        return self.driver.find_elements(*self.product_price)

    def get_all_product_image(self):
        return self.driver.find_elements(*self.product_image)

    def get_all_product_count(self):
        """获得商品页面的商品数量"""
        names = set()
        last_size = 0
        no_change = 0

        while True:
            elements = self.get_all_product_title()
            for el in elements:
                try:
                    if el.text:
                        names.add(el.text)
                except Exception:
                    pass

            if len(names) == last_size:
                no_change += 1
                if no_change >= 2:
                    break
            else:
                no_change = 0
            last_size = len(names)

            self.swipe_once()

        return len(names)

    def click_first_product_in_detail(self):
        """点击第一个商品进详情页"""
        self.wait.until(
            EC.visibility_of_element_located(self.first_product_detail)
        ).click()

    def get_first_product_name(self):
        """获得第一个商品的名字"""
        names = self.get_all_product_title()
        if names:
            return names[0].get_attribute("text")
        raise Exception("没有找到商品名称")

    def get_first_product_price(self):
        """获得第一个商品的价格"""
        prices = self.driver.find_elements(*self.product_price)
        if prices:
            return prices[0].get_attribute("text")
        raise Exception("没有找到商品价格")

    # 购物车
    def is_first_product_btn_add_to_cart(self):
        """验证：第一个商品是否成功加入购物车"""
        remove_btn = self.get_all_remove_btn()
        if not remove_btn:
            return False
        return remove_btn[0].get_attribute("content-desc") == "test-REMOVE"

    def get_cart_count(self):
        """获得购物车右上角的数字"""
        try:
            return int(self.driver.find_element(*self.cart_count).text)
        except Exception:
            return 0