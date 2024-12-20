from math import log
import sys
import os
import webview
import subprocess
import time
import threading
import win32gui
import win32con
import win32process
import logging

# 配置日志
log_file = os.path.join(
    (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(__file__)
    ),
    "app.log",
)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("wecharm")


def get_wechat_window_rect():
    """获取微信窗口的位置和大小"""
    wechat_handle = win32gui.FindWindow("WeChatMainWndForPC", None)
    if wechat_handle != 0:
        rect = win32gui.GetWindowRect(wechat_handle)
        x, y, width, height = rect
        logger.debug(
            "微信窗口位置：({}, {})，尺寸：{} x {}".format(x, y, width - x, height - y)
        )
    else:
        logger.debug("未找到微信窗口")


def check_wechat_active(callback):
    """检测微信窗口是否处于激活状态"""
    while True:
        active_window_handle = win32gui.GetForegroundWindow()
        active_window_class = win32gui.GetClassName(active_window_handle)
        if active_window_class == "WeChatMainWndForPC":
            callback(True)
        else:
            callback(False)
        time.sleep(1)


def get_wechat_handle():
    """获取微信窗口句柄"""
    return win32gui.FindWindow("WeChatMainWndForPC", None)


def is_wechat_minimized():
    """检查微信窗口是否最小化"""
    handle = get_wechat_handle()
    if handle == 0:
        return True
    return win32gui.IsIconic(handle)


def is_wechat_active():
    """检查微信窗口是否处于激活状态"""
    try:
        wechat_handle = get_wechat_handle()
        if not wechat_handle:
            return False

        # 获取当前激活窗口
        active_window = win32gui.GetForegroundWindow()
        # 如果当前激活窗口是微信或者是我们的窗口，都认为是活跃状态
        our_window = win32gui.FindWindow(None, "微言妙语")
        return active_window in (wechat_handle, our_window)
    except Exception as e:
        logging.error(f"检查微信窗口状态时出错: {str(e)}")
        return False


def attach_window_to_wechat(window_handle):
    """将窗口吸附到微信窗口右侧"""
    if not window_handle:
        logging.error("无效的应用窗口句柄")
        return False

    wechat_handle = get_wechat_handle()
    if not wechat_handle:
        logging.error("未找到微信窗口，请确保微信已经启动")
        return False

    logging.info(f"获取到微信窗口句柄: {wechat_handle}")
    # 获取微信窗口位置和大小
    wx, wy, wr, wb = win32gui.GetWindowRect(wechat_handle)
    wechat_height = wb - wy

    # 固定窗口宽度为 650
    window_width = 650

    # 计算新位置（微信窗口右侧，完全贴合）
    new_x = wr - 1  # 减去 Windows 窗口边框宽度，确保完全贴合
    new_y = wy

    # 设置窗口位置和大小
    win32gui.SetWindowPos(
        window_handle,
        win32con.HWND_TOP,
        new_x,
        new_y,
        window_width,
        wechat_height,  # 使高度与微信窗口完全一致
        win32con.SWP_SHOWWINDOW | win32con.SWP_FRAMECHANGED,
    )
    return True


def sync_window_with_wechat(window_handle):
    """同步窗口显示状态与微信窗口"""
    # is_minimized = is_wechat_minimized()
    is_active = is_wechat_active()
    if is_active:
        win32gui.ShowWindow(window_handle, win32con.SW_SHOW)
        # 只使用 SetWindowPos 来保持窗口在顶层，而不改变焦点
        win32gui.SetWindowPos(
            window_handle,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW,
        )
        attach_window_to_wechat(window_handle)
    else:
        win32gui.ShowWindow(window_handle, win32con.SW_HIDE)


def start_backend():
    """启动后端服务"""
    try:
        if getattr(sys, "frozen", False):
            # 如果是打包后的环境
            backend_dir = os.path.join(
                os.path.dirname(sys.executable), "_internal", "backend"
            )
            if not os.path.exists(backend_dir):
                logging.error(f"后端目录不存在: {backend_dir}")
                return

            backend_src = os.path.join(backend_dir, "src")
            if not os.path.exists(backend_src):
                logging.error(f"后端源码目录不存在: {backend_src}")
                return

            logging.info(f"启动后端服务，路径: {backend_src}")
            # 在打包环境中，直接导入后端模块
            sys.path.append(backend_src)
            import app

            threading.Thread(
                target=app.app.run,
                kwargs={"host": "0.0.0.0", "port": 5000},
                daemon=True,
            ).start()
        else:
            backend_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "backend", "src", "app.py"
            )
            if not os.path.exists(backend_path):
                logging.error(f"后端脚本不存在: {backend_path}")
                return

            logging.info(f"启动后端服务，路径: {backend_path}")
            # 开发环境下使用当前 python 解释器
            subprocess.Popen([sys.executable, backend_path])
        # 等待后端启动
        time.sleep(2)
    except Exception as e:
        logging.error(f"启动后端服务失败: {str(e)}")
        raise


def monitor_window(window):
    """监控窗口状态的线程函数"""
    # 等待窗口完全创建
    time.sleep(1)

    # 获取窗口句柄
    window_handle = win32gui.FindWindow(None, "微言妙语")

    while True:
        sync_window_with_wechat(window_handle)
        time.sleep(0.1)  # 每100ms检查一次


class Api:
    def close_window(self):
        """关闭窗口并退出程序"""
        logger.debug("关闭窗口并退出程序")
        window.destroy()
        sys.exit(0)


def main():
    global window
    try:
        # 检查微信是否已启动
        if get_wechat_handle() == 0:
            win32gui.MessageBox(
                None,
                "请先启动微信，再打开此程序",
                "提示",
                win32con.MB_OK | win32con.MB_ICONINFORMATION,
            )
            sys.exit(1)

        # 启动后端服务
        start_backend()

        # 创建窗口
        api = Api()
        window = webview.create_window(
            title="微言妙语",
            url="http://127.0.0.1:5000/chat-app/",
            width=650,
            height=768,
            resizable=False,
            frameless=True,
            js_api=api,  # 绑定 API
        )

        # 启动监控线程
        monitor_thread = threading.Thread(
            target=monitor_window, args=(window,), daemon=True
        )
        monitor_thread.start()

        # 启动主窗口
        webview.start()
    except Exception as e:
        logging.error(f"启动应用时出错: {str(e)}")


if __name__ == "__main__":
    main()
