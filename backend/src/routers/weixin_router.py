from flask import Blueprint, jsonify, request
import json
from utils.file_helper import get_file_path
import os
from utils.weixin_utils import WeixinUtils

bp = Blueprint("weixin", __name__)


@bp.route("/send_msg", methods=["POST"])
def send_msg():
    """发送消息给微信当前的聊天窗口"""
    # 从请求中获取msg参数
    msg = request.json.get("msg")
    if not msg:
        return jsonify({"error": "Missing 'msg' parameter"}), 400

    # 获取当前聊天窗口的名称
    WeixinUtils.send_msg(msg)
    return jsonify({"message": "Message sent successfully"}), 200
