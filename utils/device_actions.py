import base64


class DeviceActions:

    def __init__(self, driver):
        self.driver = driver

    # 系统按键
    def press_back(self):   # back
        self.driver.press_keycode(4)

    def press_home(self):   # home
        self.driver.press_keycode(3)

    def press_menu(self):   # menu
        self.driver.press_keycode(82)

    # 屏幕方向切换
    def rotate_landscape(self):     # 把设备切换横屏
        self.driver.orientation = "LANDSCAPE"

    def rotate_portrait(self):      # 切回竖屏
        self.driver.orientation = "PORTRAIT"

    def get_orientation(self):      # 读取当前是横屏还是竖屏
        return self.driver.orientation

    # 设备锁屏/解锁
    def lock_device(self, second=5):
        self.driver.lock(second)

    def unlock_device(self):
        self.driver.unlock()

    def is_locked(self):    # 常用来做断言，确认锁屏/解锁状态是否符合预期
        return self.driver.is_locked()

    # 通知栏操作
    def open_notifications(self):
        self.driver.open_notifications()

    # 隐藏键盘
    def hide_keyboard(self):
        self.driver.hide_keyboard()

    # 模拟地理位置
    def set_location(self, latitude, longitude, altitude=0):    # 纬度、经度、海拔高度
        self.driver.set_location(latitude, longitude, altitude)

    def get_location(self):     # 读取设备当前记录的坐标
        return self.driver.location

    # 网络状态切换
    def set_network_airplane_mode(self):
        self.driver.set_network_connection(1)  # 1 = 仅飞行模式

    def set_network_wifi_only(self):
        self.driver.set_network_connection(2)  # 2 = 仅WiFi

    def set_network_data_only(self):
        self.driver.set_network_connection(4)  # 4 = 仅移动数据

    def set_network_all(self):
        self.driver.set_network_connection(6)  # 6 = WiFi + 数据都开

    def get_network_connection(self):
        return self.driver.network_connection

    def swipe_once(self):
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = size["height"] * 0.7
        end_y = size["height"] * 0.2
        self.driver.swipe(
            start_x, start_y, start_x, end_y, 1000)

