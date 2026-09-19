from pages.product_page import ProductPage
from utils.device_actions import DeviceActions
from pages.login_page import LoginPage
from pages.cart_page import CartPage


def test_lock_interrupt(login_in_driver):
    """购物车中断-锁屏恢复"""
    product = ProductPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    assert product.get_cart_count() == 1

    device.lock_device()
    assert product.get_cart_count() == 1


def test_background_interrupt(login_in_driver):
    """购物车中断-切后台恢复"""
    product = ProductPage(login_in_driver)

    product.get_all_add_to_car_btn()[0].click()
    assert product.get_cart_count() == 1

    login_in_driver.background_app(3)
    assert product.get_cart_count() == 1


def test_orientation_products_page(login_in_driver):
    """商品列表页-固定竖屏适配验证

    被测App在AndroidManifest中锁定为竖屏（不支持横屏），故本用例不断言
    "布局随横屏改变"，而是验证适配的真实预期：请求切到横屏后，App仍稳定
    保持竖屏、页面不崩溃不错位，关键内容正常展示且可继续操作。
    """
    login = LoginPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    # 旋转前基线：确认在商品列表页且为竖屏
    assert login.is_on_product_page() is True
    assert device.get_orientation() == "PORTRAIT"

    # 请求切到横屏：App锁定竖屏，窗口方向应仍为竖屏
    device.rotate_landscape()
    assert device.get_orientation() == "PORTRAIT"

    # 核心业务价值：页面未崩溃、不错位，内容照常展示可用
    assert login.is_on_product_page() is True

    # 切回竖屏，状态恢复正常
    device.rotate_portrait()
    assert login.is_on_product_page() is True


def test_orientation_cart_page(login_in_driver):
    """购物车页-固定竖屏适配验证

    同商品列表页：App锁定竖屏。验证横屏请求下购物车内容不丢失、不错位、
    不崩溃，切回竖屏后状态恢复。
    """
    product = ProductPage(login_in_driver)
    cart = CartPage(login_in_driver)
    device = DeviceActions(login_in_driver)

    # 加入购物车并进入购物车页
    product.get_all_add_to_car_btn()[0].click()
    product.open_cart()
    cart.wait_for_cart_page_loaded()
    assert cart.is_on_cart_page() is True

    before_count = cart.get_all_items_count()

    # 请求横屏后仍锁定竖屏，购物车内容不丢失
    device.rotate_landscape()
    assert device.get_orientation() == "PORTRAIT"
    assert cart.is_on_cart_page() is True
    assert cart.get_all_items_count() == before_count

    # 切回竖屏
    device.rotate_portrait()
    assert cart.is_on_cart_page() is True