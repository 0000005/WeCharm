from wxauto import WeChat
from .time_utils import get_current_time
import pythoncom
import contextlib


@contextlib.contextmanager
def com_initializer():
    """
    一个 context manager，用于初始化/释放 COM 组件
    """
    pythoncom.CoInitialize()
    try:
        yield
    finally:
        pythoncom.CoUninitialize()


class WeChatSingleton:
    """
    一个单例类，提供一个唯一的 WeChat 对象
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        获取 WeChat 对象的单例

        Returns:
            WeChat: WeChat 对象的单例
        """
        if cls._instance is None:
            cls._instance = WeChat()
        return cls._instance


class WeixinUtils:
    @staticmethod
    def get_chat_history(max_messages: int = None) -> str:
        """
        从 wxauto 中获取当前窗口的聊天记录，并且返回格式化后的字符串

        Args:
            max_messages (int, optional): 最大返回的消息数量，从最新到最旧。默认为 None，表示返回所有消息。

        Returns:
            str: 格式化后的聊天记录
            list:所有的聊天记录
        """
        with com_initializer():
            wx = WeChatSingleton.get_instance()
            # 获取当前窗口的聊天记录，返回值是一个数组
            msgs = wx.GetAllMessage()

            # 如果指定了最大消息数，则只取最新的 N 条消息
            if max_messages is not None:
                msgs = msgs[-max_messages:]

            result = []  # Create a list to store formatted messages
            for msg in msgs:
                if msg.type == "sys":
                    result.append(f"【sys】{msg.content}")

                elif msg.type == "friend":
                    result.append(f"【{msg.sender}】：{msg.content}")

                elif msg.type == "self":
                    result.append(f"【我】：{msg.content}")

                elif msg.type == "time":
                    result.append(f"【time】{msg.time}")

                elif msg.type == "recall":
                    result.append(f"【recall】{msg.content}")

            # Join all messages with newlines
            chat_history_str = "\n".join(result)

            return chat_history_str, msgs

    @staticmethod
    def get_current_chat_name():
        """
        从 wxauto 中获取当前聊天窗口的名称

        Returns:
            str: 当前聊天窗口的名称
        """
        with com_initializer():
            wx = WeChatSingleton.get_instance()
            return wx.CurrentChat()

    @staticmethod
    def send_msg(msg: str):
        """
        从 wxauto 中发送消息到当前聊天窗口

        Args:
            msg (str): 要发送的消息
        """
        with com_initializer():
            wx = WeChatSingleton.get_instance()
            wx.SendMsg(msg)

    @staticmethod
    def get_all_new_message(max_round=10):
        """
        从 wxauto 中获取所有新消息

        Args:
            max_round (int): 最大获取次数  * 这里是为了避免某几个窗口一直有新消息，导致无法停止

        Returns:    
            list: 所有新消息的列表
        """
        with com_initializer():
            wx = WeChatSingleton.get_instance()
            return wx.GetAllNewMessage(max_round)