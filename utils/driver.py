from appium import webdriver
from appium.options.android import UiAutomator2Options
import os


def get_driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = os.environ.get("Device_name", "emulator-5554")
    options.automation_name = "UiAutomator2"

    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = "com.swaglabsmobileapp.MainActivity"

    options.no_reset = False

    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
    if chromedriver_path:
        options.set_capability('appium:chromedriverExecutable', chromedriver_path)

    options.set_capability('appium:uiautomator2ServerLaunchTimeout', 120000)

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    return driver