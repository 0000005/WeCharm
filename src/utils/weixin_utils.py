from wxauto import WeChat


class WeixinUtils:
    @staticmethod
    def get_chat_history(max_messages: int = None) -> str:
        """
        从 wxauto 中获取当前窗口的聊天记录，并且返回格式化后的字符串

        Args:
            max_messages (int, optional): 最大返回的消息数量，从最新到最旧。默认为 None，表示返回所有消息。

        Returns:
            str: 格式化后的聊天记录
        """
        wx = WeChat()
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
                result.append(f"【{msg.sender.ljust(20)}】：{msg.content}")

            elif msg.type == "self":
                result.append(f"【self】：{msg.content}")

            elif msg.type == "time":
                result.append(f"【time】{msg.time}")

            elif msg.type == "recall":
                result.append(f"【recall】{msg.content}")

        # Join all messages with newlines
        chat_history = "\n".join(result)

        return chat_history
