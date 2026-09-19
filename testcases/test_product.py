from pages.product_page import ProductPage
from pages.product_detail_page import ProductDetailPage


def test_product_count(login_in_driver):
    """商品数量正确"""
    product = ProductPage(login_in_driver)

    product_count = product.get_all_product_count()
    assert product_count == 6


def test_sort_by_name(login_in_driver):
    """按名称升序排序"""
    product = ProductPage(login_in_driver)

    product.click_sort_dropdown()
    product.click_sort_by_name()

    elements = product.get_all_product_title()
    actual_names = [el.text for el in elements]

    assert actual_names == sorted(actual_names)


def test_sort_by_price(login_in_driver):
    """按价格升序排序"""
    product = ProductPage(login_in_driver)

    product.click_sort_dropdown()
    product.click_sort_by_price()

    elements = product.get_all_product_price()
    actual_price = [el.text for el in elements]

    assert actual_price == sorted(actual_price)


def test_show_product_detail(login_in_driver):
    """商品详情页展示"""
    product = ProductPage(login_in_driver)
    detail = ProductDetailPage(login_in_driver)

    product.click_first_product_in_detail()

    desc = detail.get_detail_desc()
    price = detail.get_detail_price()
    image = detail.get_detail_image()

    assert desc != "", "商品描述为空"
    assert price != "", "商品价格为空"
    assert image is not None, "商品图片缺失"