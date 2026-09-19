from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.product_detail_page import ProductDetailPage
from pages.login_page import LoginPage
from utils.device_actions import DeviceActions
import time


def test_add_cart_by_list(login_in_driver):
    """	在商品列表页加入购物车"""
    product = ProductPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()

    assert product.is_first_product_btn_add_to_cart() is True
    assert product.get_cart_count() == 1


def test_add_cart_by_detail(login_in_driver):
    """详情页加入购物车"""
    product = ProductPage(login_in_driver)
    detail = ProductDetailPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    product.click_first_product_in_detail()
    device.swipe_once()
    detail.click_add_btn()

    assert detail.is_add_to_cart() is True
    assert product.get_cart_count() == 1


def test_check_cart_by_product_exist(login_in_driver):
    """有商品加入购物车时查看"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()

    product_name = product.get_first_product_name()
    product_price = product.get_first_product_price()

    product.open_cart()
    time.sleep(2)

    assert cart.get_first_cart_item_name() == product_name
    assert cart.get_first_cart_item_price() == product_price


def test_cart_null(login_in_driver):
    """购物车为空时查看"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)

    product.open_cart()

    time.sleep(2)

    assert cart.is_cart_empty() is True


def test_add_more_carts(login_in_driver):
    """添加多个商品到购物车"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(2)

    cart_count = cart.get_all_items_count()

    assert product.get_cart_count() == 2
    assert cart_count == 2


def test_remove_carts(login_in_driver):
    """移除购物车商品"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    product.get_all_add_to_car_btn()[0].click()

    before_count = product.get_cart_count()

    product.open_cart()
    cart.remove_first_product()
    time.sleep(2)
    after_count = product.get_cart_count()

    assert before_count == after_count+1


def test_continue_shopping(login_in_driver):
    """继续购物返回列表"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    login = LoginPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    before_count = product.get_cart_count()
    product.open_cart()
    cart.click_continue_shopping()
    time.sleep(2)
    after_count = product.get_cart_count()

    assert before_count == after_count
    assert login.is_on_product_page() is True