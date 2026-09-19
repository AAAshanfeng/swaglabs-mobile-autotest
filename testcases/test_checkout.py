from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.checkout_info_page import CheckoutPage
from utils.device_actions import DeviceActions
import time


def test_checkout_success(login_in_driver):
    """正常完整下单流程"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    checkout = CheckoutPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    expect_name = product.get_first_product_name()
    expect_price = product.get_first_product_price()
    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(1)
    assert product.get_cart_count() == 1
    assert cart.get_first_cart_item_name() == expect_name
    assert cart.get_first_cart_item_price() == expect_price

    cart.click_checkout()
    checkout.input_firstname("test")
    checkout.input_lastname("Doe")
    checkout.input_zip("123456")
    checkout.click_continue_btn()

    time.sleep(1)

    item_total = checkout.get_item_total()
    tax = checkout.get_tax()
    total = checkout.get_total()

    assert checkout.get_item_name() == expect_name
    assert checkout.get_item_desc() != ""
    assert checkout.get_item_price() == expect_price
    assert round(item_total + tax, 2) == round(total, 2)

    device.swipe_once()
    checkout.click_finish_btn()
    time.sleep(1)
    assert checkout.is_complete_page() is True

    checkout.click_back_home_btn()
    product.open_cart()

    # cart.wait_for_cart_page_loaded()
    assert cart.is_on_cart_page() is True
    assert cart.is_cart_empty() is True


def test_firstname_null(login_in_driver):
    """收货信息：姓为空"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    checkout = CheckoutPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(1)

    cart.click_checkout()
    checkout.input_lastname("Doe")
    checkout.input_zip("123456")
    checkout.click_continue_btn()

    assert checkout.get_error_message() is not None


def test_lastname_null(login_in_driver):
    """收货信息：名为空"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    checkout = CheckoutPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(1)

    cart.click_checkout()
    checkout.input_firstname("test")
    checkout.input_zip("123456")
    checkout.click_continue_btn()

    assert checkout.get_error_message() is not None


def test_zipcode_null(login_in_driver):
    """收货信息：邮编为空"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    checkout = CheckoutPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(1)

    cart.click_checkout()
    checkout.input_firstname("test")
    checkout.input_lastname("Doe")
    checkout.click_continue_btn()

    assert checkout.get_error_message() is not None


def test_cancel_checkout(login_in_driver):
    """结账流程中取消"""
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    checkout = CheckoutPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    expect_name = product.get_first_product_name()
    expect_price = product.get_first_product_price()
    product.get_all_add_to_car_btn()[0].click()

    product.open_cart()
    time.sleep(1)

    cart.click_checkout()
    checkout.fill_checkout_info("test", "Doe", "123456")
    checkout.click_continue_btn()

    time.sleep(1)
    device.swipe_once()
    checkout.click_cancel_btn()

    product = ProductPage(login_in_driver)
    product.open_cart()

    assert product.get_cart_count() == 1
    assert cart.get_first_cart_item_name() == expect_name
    assert cart.get_first_cart_item_price() == expect_price