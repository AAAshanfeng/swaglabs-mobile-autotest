from appium import webdriver
from appium.options.android import UiAutomator2Options
import os


def get_driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = os.environ.get("Device_name", "emulator-5554")  # 从系统环境变量中读取配置
    options.automation_name = "UiAutomator2"

    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = "com.swaglabsmobileapp.MainActivity"

    options.no_reset = False    # 启动前是否重置应用状态 False：重置

    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")     # WebView才需要
    if chromedriver_path:   # 把 ChromeDriver 路径添加到 Appium 配置中
        options.set_capability('appium:chromedriverExecutable', chromedriver_path)

    # 配置 UiAutomator2 服务的启动超时时间：120秒
    options.set_capability('appium:uiautomator2ServerLaunchTimeout', 120000)

    # 请求 Appium Server 创建自动化会话
    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    return driver