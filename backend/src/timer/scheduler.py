import threading
import time
import logging
from utils.weixin_utils import WeixinUtils

logger = logging.getLogger("wecharm")

class Timer:
    def __init__(self):
        self._running = False
        self._thread = None

    def _run(self):
        while self._running:
            try:
                # 这里添加你的定时任务逻辑
                chat_name = WeixinUtils.get_current_chat_name()
                # msg_list = WeixinUtils.get_all_new_message(1)
                logger.info("current chat name: " + chat_name )
                
            except Exception as e:
                logger.error(f"Timer task error: {str(e)}")
            
            time.sleep(1)  # 休眠1秒

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True  # 设置为守护线程，这样主程序退出时线程会自动结束
            self._thread.start()
            logger.info("Timer started")

    def stop(self):
        if self._running:
            self._running = False
            if self._thread:
                self._thread.join()
            logger.info("Timer stopped")

# 创建定时器实例
timer = Timer()
