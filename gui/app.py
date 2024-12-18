import webview
import subprocess
import time
import sys
import os


def start_backend():
    backend_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "backend", "src", "app.py"
    )
    # 使用 python 命令启动后端
    subprocess.Popen([sys.executable, backend_path])
    # 等待后端启动
    time.sleep(2)


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
    )
    webview.start()


if __name__ == "__main__":
    main()
