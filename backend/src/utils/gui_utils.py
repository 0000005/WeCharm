import win32gui
import win32con
import time


def get_wechat_window_rect():
    """
    Retrieves the window rectangle (position and size) of the WeChat desktop application.

    This function uses the Windows API to find the WeChat main window by its class name
    and then obtains its screen coordinates and dimensions.

    Returns:
        tuple or None: A tuple containing (x, y, width, height) of the WeChat window if found,
                       or None if the WeChat window is not detected.
                       - x: x-coordinate of the window's top-left corner
                       - y: y-coordinate of the window's top-left corner
                       - width: width of the window
                       - height: height of the window

    Side Effects:
        - Prints the window position and size to the console if the window is found
        - Prints a message if no WeChat window is detected

    Note:
        Requires the `win32gui` module to interact with Windows GUI elements.
    """
    # 通过窗口类名找到微信主窗口的句柄
    wechat_handle = win32gui.FindWindow("WeChatMainWndForPC", None)

    if wechat_handle != 0:
        # 获取微信主窗口的位置和大小信息
        rect = win32gui.GetWindowRect(wechat_handle)
        x, y, width, height = rect

        print(
            "微信窗口位置：({}, {})，尺寸：{} x {}".format(x, y, width - x, height - y)
        )

        # 在这里可以根据微信窗口的位置信息计算出侧边栏的位置信息

    else:
        print("未找到微信窗口")


# 定义一个函数来检测微信窗口是否处于激活状态，并接受一个回调函数作为参数
def check_wechat_active(callback):
    while True:
        # 获取当前活动窗口句柄
        active_window_handle = win32gui.GetForegroundWindow()

        # 获取当前活动窗口类名
        active_window_class = win32gui.GetClassName(active_window_handle)

        if active_window_class == "WeChatMainWndForPC":
            callback(True)  # 调用回调函数，传递True表示微信窗口处于激活状态
        else:
            callback(False)  # 调用回调函数，传递False表示微信窗口未处于激活状态

        time.sleep(1)  # 每秒检测一次微信窗口是否处于激活状态
