from pages.login_page import LoginPage
from logging_config import logger


def test_login_success(driver):
    """登录成功"""
    login = LoginPage(driver)

    login.input_username("standard_user")
    login.input_password("secret_sauce")
    login.click_login_btn()

    assert login.is_on_product_page() is True


def test_login_wrong_password(driver):
    """密码错误"""
    login = LoginPage(driver)

    login.input_username("standard_user")
    login.input_password("wrong_password")
    login.click_login_btn()

    assert "password" in login.get_error_message().lower()


def test_login_wrong_username(driver):
    """用户不存在	"""
    login = LoginPage(driver)

    login.input_username("wrong_username")
    login.input_password("secret_sauce")
    login.click_login_btn()

    assert "username" in login.get_error_message().lower()


def test_null_password(driver):
    """密码为空"""
    login = LoginPage(driver)

    login.input_username("standard_user")
    login.click_login_btn()

    assert "password" in login.get_error_message().lower()


def test_null_username(driver):
    """用户名为空"""
    login = LoginPage(driver)

    login.input_password("secret_sauce")
    login.click_login_btn()

    assert "username" in login.get_error_message().lower()


def test_null_username_password(driver):
    """用户名与密码为空"""
    login = LoginPage(driver)

    login.click_login_btn()

    assert "username" in login.get_error_message().lower()


def test_locked_user(driver):
    """锁定账户登录"""
    login = LoginPage(driver)

    login.input_username("locked_out_user")
    login.input_password("secret_sauce")
    login.click_login_btn()

    assert "locked" in login.get_error_message().lower()