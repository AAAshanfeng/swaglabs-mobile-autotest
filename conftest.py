import pytest
from utils.driver import get_driver
from pages.login_page import LoginPage
import subprocess
import os
import time
from logging_config import logger


@pytest.fixture
def driver():

    driver = get_driver()

    yield driver

    driver.quit()


@pytest.fixture()
def login_in_driver(driver):
    login = LoginPage(driver)

    login.input_username("standard_user")
    login.input_password("secret_sauce")
    logger.info("开始登录")
    login.click_login_btn()

    assert login.is_on_product_page(), "登录失败，未跳转到商品页"
    logger.info("登录成功")

    return driver


@pytest.fixture()
def reset_permission(driver):
    subprocess.run(
        ["adb", "shell", "pm", "clear", "com.swaglabsmobileapp"],
        check=True  # ADB 命令以非零状态码退出会抛出异常
    )
    driver.activate_app("com.swaglabsmobileapp")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("login_in_driver")

        if driver:
            screenshots_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "screenshots"
            )
            os.makedirs(screenshots_dir, exist_ok=True)

            filename = os.path.join(
                screenshots_dir,
                f"{item.name}_{int(time.time())}.png"
            )
            driver.save_screenshot(filename)