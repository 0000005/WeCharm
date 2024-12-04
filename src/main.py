from config.prompts import get_prompt
from langchain_openai import ChatOpenAI
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_BASE_URL
from wxauto import *
from utils.llm_utils import LLMUtils
from utils.weixin_utils import WeixinUtils
from views.main_window import main_frame
import wx

# Example usage
if __name__ == "__main__":

    app = wx.App()
    frame = main_frame(None)
    frame.Show()
    app.MainLoop()
