import sys
import os
import webview
import subprocess
import time
import threading
import win32gui
import win32con
import logging

# 配置日志
log_file = os.path.join(os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(__file__), "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("weixin_copilot")


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


def attach_window_to_wechat(window_handle):
    """将窗口吸附到微信窗口右侧"""
    wechat_handle = get_wechat_handle()
    if wechat_handle == 0:
        return False

    # 获取微信窗口位置和大小
    wx, wy, wr, wb = win32gui.GetWindowRect(wechat_handle)
    wechat_height = wb - wy

    # 固定窗口宽度为 550
    window_width = 550

    # 计算新位置（微信窗口右侧，完全贴合）
    new_x = wr - 8  # 减去 Windows 窗口边框宽度，确保完全贴合
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
    is_minimized = is_wechat_minimized()
    if is_minimized:
        win32gui.ShowWindow(window_handle, win32con.SW_HIDE)
    else:
        win32gui.ShowWindow(window_handle, win32con.SW_SHOW)
        attach_window_to_wechat(window_handle)


def start_backend():
    """启动后端服务"""
    try:
        if getattr(sys, "frozen", False):
            # 如果是打包后的环境
            backend_dir = os.path.join(os.path.dirname(sys.executable), "_internal", "backend")
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
            threading.Thread(target=app.app.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True).start()
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
        time.sleep(0.1)  # 每500ms检查一次


def main():
    # 启动后端服务
    start_backend()

    # 创建窗口
    window = webview.create_window(
        title="WeChat Copilot",
        url="http://127.0.0.1:5000/chat-app/",
        width=550,
        height=768,
        resizable=True,
        frameless=True,
    )

    # 启动监控线程
    monitor_thread = threading.Thread(
        target=monitor_window, args=(window,), daemon=True
    )
    monitor_thread.start()

    # 启动主窗口
    webview.start()


if __name__ == "__main__":
    main()