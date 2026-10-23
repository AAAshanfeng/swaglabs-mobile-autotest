from pages.product_page import ProductPage
from pages.menu_page import MenuPage
from pages.permission import PermissionPage
from pages.login_page import LoginPage
import time
import subprocess
import pytest


@pytest.mark.parametrize(
    "btn_method",
    [
        "click_location_btn", "click_QR_code_btn"
    ],
    ids=["location", "QR code"],
)
def test_permission_first_request(reset_permission, login_in_driver, btn_method):
    """首次请求权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    getattr(menu, btn_method)()

    assert permission.is_permission_dialog_exist() is True


@pytest.mark.parametrize(
    "btn_method",
    [
        "click_location_btn", "click_QR_code_btn"
    ],
    ids=["location", "QR code"],
)
def test_permission_allow(reset_permission, login_in_driver, btn_method):
    """允许权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    getattr(menu, btn_method)()
    permission.click_permission_allow_foreground_only()
    assert permission.is_permission_dialog_exist() is False

    result = subprocess.run(
        ["adb", "shell", "dumpsys", "package", "com.swaglabsmobileapp"],
        capture_output=True, text=True
    )
    assert "granted=true" in result.stdout


@pytest.mark.parametrize(
    "btn_method, find_permission",
    [
        ("click_location_btn", "ACCESS_FINE_LOCATION"),
        ("click_QR_code_btn", "CAMERA"),
    ],
    ids=["location", "QR code"],
)
def test_permission_deny(reset_permission, login_in_driver, btn_method, find_permission):
    """拒绝权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    getattr(menu, btn_method)()
    permission.click_permission_deny()
    assert permission.is_permission_dialog_exist() is False

    result = subprocess.run(
        ["adb", "shell", "dumpsys", "package", "com.swaglabsmobileapp"],
        capture_output=True, text=True
    )
    target_line = ""
    for line in result.stdout.splitlines():
        if find_permission in line and "granted=" in line:
            target_line = line
            break

    assert target_line, f'dumpsys 未找到 {find_permission} 的状态行'
    assert "granted=true" not in target_line


@pytest.mark.parametrize(
    "btn_method",
    [
        "click_location_btn", "click_QR_code_btn"
    ],
    ids=["location", "QR code"],
)
def test_permission_once(reset_permission, login_in_driver, btn_method):
    """点击"仅一次"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)
    login = LoginPage(login_in_driver)

    product.open_menu()
    getattr(menu, btn_method)()
    permission.click_permission_once()

    result = subprocess.run(
        ["adb", "shell", "dumpsys", "package", "com.swaglabsmobileapp"],
        capture_output=True, text=True
    )
    assert "granted=true" in result.stdout

    login_in_driver.terminate_app("com.swaglabsmobileapp")
    time.sleep(10)
    login_in_driver.activate_app("com.swaglabsmobileapp")
    login.login("standard_user", "secret_sauce")

    product.open_menu()
    getattr(menu, btn_method)()
    time.sleep(2)
    assert permission.is_permission_dialog_exist() is True


@pytest.mark.parametrize(
    "btn_method, find_permission",
    [
        ("click_location_btn", "android.permission.ACCESS_FINE_LOCATION"),
        ("click_QR_code_btn", "android.permission.CAMERA"),
    ],
    ids=["location", "QR code"],
)
def test_permission_revoked_manually(reset_permission, login_in_driver, btn_method, find_permission):
    """手动撤销权限 """
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)
    login = LoginPage(login_in_driver)

    product.open_menu()
    getattr(menu, btn_method)()
    permission.click_permission_allow_foreground_only()

    subprocess.run([
        "adb", "shell", "pm", "revoke",
        "com.swaglabsmobileapp",
        find_permission
    ])

    subprocess.run([
        "adb", "shell", "pm", "clear",
        "com.swaglabsmobileapp"
    ])

    login_in_driver.terminate_app("com.swaglabsmobileapp")
    login_in_driver.activate_app("com.swaglabsmobileapp")
    login.login("standard_user", "secret_sauce")

    product.open_menu()
    getattr(menu, btn_method)()
    time.sleep(2)
    assert permission.is_permission_dialog_exist() is True


def test_drawing_first_request(reset_permission, login_in_driver):
    """Drawing保存-首次请求存储权限弹窗"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    menu.click_drawing_btn()
    time.sleep(2)

    permission.drawing_line(400, 1000, 500, 1800)
    permission.click_draw_save()

    assert permission.is_permission_dialog_exist() is True


def test_drawing_permission_allow(reset_permission, login_in_driver):
    """Drawing保存-允许存储权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    menu.click_drawing_btn()
    time.sleep(2)
    permission.drawing_line(400, 1000, 500, 1800)
    permission.click_draw_save()
    permission.click_permission_allow()
    assert permission.is_permission_dialog_exist() is False

    result = subprocess.run(
        ["adb", "shell", "dumpsys", "package", "com.swaglabsmobileapp"],
        capture_output=True, text=True
    )
    assert "granted=true" in result.stdout


def test_drawing_permission_deny(reset_permission, login_in_driver):
    """Drawing保存-拒绝存储权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)

    product.open_menu()
    menu.click_drawing_btn()
    time.sleep(2)
    permission.drawing_line(400, 1000, 500, 1800)
    permission.click_draw_save()
    permission.click_permission_deny()
    assert permission.is_permission_dialog_exist() is False

    result = subprocess.run(
        ["adb", "shell", "dumpsys", "package", "com.swaglabsmobileapp"],
        capture_output=True, text=True
    )
    target_line = ""
    for line in result.stdout.splitlines():
        if "READ_MEDIA_IMAGES" in line and "granted=" in line:
            target_line = line
            break

    assert target_line, 'dumpsys 未找到 READ_MEDIA_IMAGES 的状态行'
    assert "granted=true" not in target_line


def test_drawing_permission_revoked_manually(reset_permission, login_in_driver):
    """Drawing保存-手动撤销存储权限"""
    product = ProductPage(login_in_driver)
    menu = MenuPage(login_in_driver)
    permission = PermissionPage(login_in_driver)
    login = LoginPage(login_in_driver)

    product.open_menu()
    menu.click_drawing_btn()
    time.sleep(2)
    permission.drawing_line(400, 1000, 500, 1800)
    permission.click_draw_save()
    permission.click_permission_allow()

    subprocess.run([
        "adb", "shell", "pm", "revoke",
        "com.swaglabsmobileapp",
        "android.permission.WRITE_EXTERNAL_STORAGE"
    ], check=True)

    login_in_driver.terminate_app("com.swaglabsmobileapp")
    login_in_driver.activate_app("com.swaglabsmobileapp")
    login.login("standard_user", "secret_sauce")

    product.open_menu()
    menu.click_drawing_btn()
    time.sleep(2)
    permission.drawing_line(400, 1000, 500, 1800)
    permission.click_draw_save()
    time.sleep(2)
    assert permission.is_drawing_permission_dialog_exist() is True