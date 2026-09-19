from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


class MenuPage(BasePage):

    webview_btn = (AppiumBy.ACCESSIBILITY_ID, "test-WEBVIEW")
    QR_code_btn = (AppiumBy.ACCESSIBILITY_ID, "test-QR CODE SCANNER")
    location_btn = (AppiumBy.ACCESSIBILITY_ID, "test-GEO LOCATION")
    drawing_btn = (AppiumBy.ACCESSIBILITY_ID, "test-DRAWING")
    logout_btn = (AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")
    reset_btn = (AppiumBy.ACCESSIBILITY_ID, "test-RESET APP STATE")

    webview_url = (AppiumBy.ACCESSIBILITY_ID, "test-enter a https url here...")
    site_btn = (AppiumBy.ACCESSIBILITY_ID, "test-GO TO SITE")
    bing_page = (AppiumBy.XPATH, '//android.webkit.WebView[@text="搜索 - Microsoft 必应"]')

    def click_webview_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.webview_btn)
        ).click()

    def click_QR_code_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.QR_code_btn)
        ).click()

    def click_location_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.location_btn)
        ).click()

    def click_drawing_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.drawing_btn)
        ).click()

    def click_logout_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.logout_btn)
        ).click()

    def click_reset_btn(self):
        self.wait.until(
            EC.element_to_be_clickable(self.reset_btn)
        ).click()

    # webview
    def input_webview_url(self, url):
        self.wait.until(
            EC.visibility_of_element_located(self.webview_url)
        ).send_keys(url)

    def click_site_btn(self):
        self.driver.find_element(*self.site_btn).click()

    def is_on_bing_page(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.bing_page)
            )
            return True
        except:
            return False