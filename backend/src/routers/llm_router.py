from flask import Blueprint, jsonify, abort, request
from utils.weixin_utils import WeixinUtils
from utils.llm_utils import LLMUtils
from models.friend_model import Friend
from models.setting_model import Settings
from utils.file_helper import get_file_path
import json
import os
import traceback
from dataclasses import asdict
import logging
import traceback

logger = logging.getLogger("wecharm")

bp = Blueprint("llm", __name__)


# 意图探索接口
# 0、先调用 weixin_utils.py 中的 get_current_chat_name() 获取当前聊天窗口的名称，作为用户昵称
# 1、先获取系统配置信息（参考setting.py）
# 2、先获取好友配置信息（参考friend.py）
# 3、获取微信聊天记录（参考weixin_utils.py）
# 4、调用llm_utils.py中的get_llm_response(prompt_type, chat_history, friend),其中 prompt_type 固定为 “生成意图”
# 返回结果的类型是：{"intent_list":[{"text":"描述方向的内容"}]}
@bp.route("/intent", methods=["GET"])
def explore_intent():
    try:

        # 0. 获取当前聊天窗口的名称
        nickname = WeixinUtils.get_current_chat_name()
        if not nickname:
            return jsonify({"error": "No active chat window"}), 400

        # 1. 获取系统配置信息
        settings_file = get_file_path("setting.json")
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
                settings = Settings(**settings_data)
        else:
            settings = Settings()  # 使用默认配置
        # 检查，如果setting中没有配置 model,baseUrl或apiKey就返回400错误
        if not settings.model or not settings.baseUrl or not settings.apiKey:
            return (
                jsonify({"error": "请先到设置界面配置正确的API地址、模型、API Key。"}),
                400,
            )

        # 2. 获取好友配置信息
        friend_file = get_file_path(f"{nickname}.json")
        if os.path.exists(friend_file):
            with open(friend_file, "r", encoding="utf-8") as f:
                friend_data = json.load(f)
                friend = Friend(**friend_data)
        else:
            friend = Friend(wechatNickname=nickname)  # 使用默认配置

        # 3. 获取微信聊天记录，使用friend.contextSize作为消息数量
        chat_history = WeixinUtils.get_chat_history(max_messages=friend.contextSize)
        if not chat_history:
            return jsonify({"error": "No chat history available"}), 400

        # 4. 调用LLM获取意图分析，传入settings参数
        response = LLMUtils.get_llm_response("生成意图", chat_history, friend, settings)

        return jsonify(asdict(response)), 200

    except Exception as e:
        # 打印错误堆栈
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# 智能回复
# 该接口是一个post接口，有一个参数：user_intent（用户意图）
# 0、先调用 weixin_utils.py 中的 get_current_chat_name() 获取当前聊天窗口的名称，作为用户昵称
# 1、先获取系统配置信息（参考setting.py）
# 2、先获取好友配置信息（参考friend.py）
# 3、获取微信聊天记录（参考weixin_utils.py）
# 4、调用llm_utils.py中的get_llm_response_with_intent(prompt_type,user_intent, chat_history, friend),其中 prompt_type 固定为 “通用”
@bp.route("/gen_reply", methods=["POST"])
def gen_reply():
    try:
        # Get user intent from request
        user_intent = request.json.get("user_intent")

        # 0. 获取当前聊天窗口的名称，作为用户昵称
        chat_name = WeixinUtils.get_current_chat_name()
        if not chat_name:
            return jsonify({"error": "No active chat window"}), 400

        # 1. 获取系统配置信息
        settings_file = get_file_path("setting.json")
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
                settings = Settings(**settings_data)
        else:
            settings = Settings()  # 使用默认配置
        # 检查，如果setting中没有配置 model,baseUrl或apiKey就返回400错误
        if not settings.model or not settings.baseUrl or not settings.apiKey:
            return (
                jsonify({"error": "请先到设置界面配置正确的API地址、模型、API Key。"}),
                400,
            )

        # 2. 获取好友配置信息
        friend_file = get_file_path(f"{chat_name}.json")
        if os.path.exists(friend_file):
            with open(friend_file, "r", encoding="utf-8") as f:
                friend_data = json.load(f)
                friend = Friend(**friend_data)
        else:
            friend = Friend(wechatNickname=chat_name)  # 使用默认配置

        # 3. 获取微信聊天记录
        chat_history = WeixinUtils.get_chat_history()
        if not chat_history:
            return jsonify({"error": "No chat history available"}), 400

        # 4. 调用LLM生成回复
        response = LLMUtils.get_llm_response_with_intent(
            "通用", user_intent, chat_history, friend, settings
        )

        return jsonify(asdict(response)), 200

    except Exception as e:
        # 打印错误堆栈
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
