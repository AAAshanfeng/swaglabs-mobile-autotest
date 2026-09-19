from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PermissionPage(BasePage):
    permission_allow_foreground_only = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
    permission_deny = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button")
    permission_only_once = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button")
    permission_allow = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")

    permission_dialog = (AppiumBy.ID, "com.android.permissioncontroller:id/grant_dialog")

    draw_clear = (AppiumBy.ACCESSIBILITY_ID, "test-CLEAR")
    draw_save = (AppiumBy.ACCESSIBILITY_ID, "test-SAVE")

    def click_permission_allow_foreground_only(self):
        self.wait.until(
            EC.element_to_be_clickable(self.permission_allow_foreground_only)
        ).click()

    def click_permission_deny(self):
        self.wait.until(
            EC.element_to_be_clickable(self.permission_deny)
        ).click()

    def click_permission_once(self):
        self.wait.until(
            EC.element_to_be_clickable(self.permission_only_once)
        ).click()

    def is_permission_dialog_exist(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.permission_dialog)
            )
            return True
        except TimeoutException:
            return False

    def drawing_line(self, x1, y1, x2, y2, duration=0.4):
        self.driver.execute_script("mobile: dragGesture", {
            "startX": x1,
            "startY": y1,
            "endX": x2,
            "endY": y2,
            "duration": duration,
        })

    def click_draw_clear(self):
        self.wait.until(
            EC.element_to_be_clickable(self.draw_clear)
        ).click()

    def click_draw_save(self):
        self.wait.until(
            EC.element_to_be_clickable(self.draw_save)
        ).click()

    def click_permission_allow(self):
        self.wait.until(
            EC.element_to_be_clickable(self.permission_allow)
        ).click()