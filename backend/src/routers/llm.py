from flask import Blueprint, jsonify, abort
from utils.weixin_utils import WeixinUtils
from utils.llm_utils import LLMUtils
from models.friend import Friend
from utils.file_helper import get_file_path
import json
import os

bp = Blueprint("llm", __name__, url_prefix="/llm")


# 意图探索接口
# 0、先调用 weixin_utils.py 中的 get_current_chat_name() 获取当前聊天窗口的名称，作为用户昵称
# 1、先获取好友配置信息（参考friend.py）
# 2、获取微信聊天记录（参考weixin_utils.py）
# 3、调用llm_utils.py中的get_llm_response(prompt_type, chat_history, friend),其中 prompt_type 固定为 “get_llm_response”
# 返回结果的类型是：{"intent_list":[{"text":"描述方向的内容"}]}


@bp.route("/intent", methods=["GET"])
def explore_intent():
    try:
        # 0. 获取当前聊天窗口的名称
        nickname = WeixinUtils.get_current_chat_name()
        if not nickname:
            return jsonify({"error": "No active chat window"}), 400

        # 1. 获取好友配置信息
        friend_file = get_file_path(f"{nickname}.json")
        if os.path.exists(friend_file):
            with open(friend_file, "r", encoding="utf-8") as f:
                friend_data = json.load(f)
                friend = Friend(**friend_data)
        else:
            friend = Friend(wechatNickname=nickname)  # 使用默认配置

        # 2. 获取微信聊天记录，使用friend.contextSize作为消息数量
        chat_history = WeixinUtils.get_chat_history(max_messages=friend.contextSize)
        if not chat_history:
            return jsonify({"error": "No chat history available"}), 400

        # 3. 调用LLM获取意图分析
        response = LLMUtils.get_llm_response("get_intent", chat_history, friend)

        return jsonify(response.dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
