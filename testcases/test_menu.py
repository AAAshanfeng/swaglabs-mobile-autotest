from pages.product_page import ProductPage
from pages.menu_page import MenuPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
import time


def test_logout(login_in_driver):
    """退出登录"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    login = LoginPage(login_in_driver)

    product.open_menu()
    menu.click_logout_btn()

    assert login.is_on_login_page() is True


def test_rest_app(login_in_driver):
    """重置App"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    login = LoginPage(login_in_driver)
    cart = CartPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    assert product.get_cart_count() == 1

    product.open_menu()
    menu.click_reset_btn()
    time.sleep(1)
    assert login.is_on_product_page() is True

    product.open_cart()
    cart.wait_for_cart_page_loaded()
    assert cart.is_cart_empty() is True


def test_webview_with_true_url(login_in_driver):
    """WebView输入正确URL跳转"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)

    product.open_menu()
    menu.click_webview_btn()

    menu.input_webview_url("www.bing.com")
    menu.click_site_btn()

    assert menu.is_on_bing_page() is True