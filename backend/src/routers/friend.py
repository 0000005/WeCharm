from flask import Blueprint, jsonify, request
import json
from utils.file_helper import get_file_path
import os
from models.friend import Friend

bp = Blueprint("friend", __name__)


@bp.route("/save", methods=["POST"])
def save_friend():
    """Save friend information to [nickname].json file"""
    try:
        friend_data = request.get_json()
        # 使用 Friend model 验证数据
        friend = Friend(**friend_data)

        if not friend.wechatNickname:
            return jsonify({"error": "WeChat nickname is required"}), 400

        # 保存好友信息到文件
        friend_file = get_file_path(f"{friend.wechatNickname}.json")
        with open(friend_file, "w", encoding="utf-8") as f:
            json.dump(friend.dict(), f, ensure_ascii=False, indent=2)

        return jsonify({"message": "Friend information saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/load/<nickname>", methods=["GET"])
def load_friend(nickname):
    """Load friend information from [nickname].json file"""
    try:
        friend_file = get_file_path(f"{nickname}.json")

        if not os.path.exists(friend_file):
            # 返回带有默认值的新 Friend 对象
            return jsonify(Friend(wechatNickname=nickname).dict()), 404

        with open(friend_file, "r", encoding="utf-8") as f:
            friend_data = json.load(f)
            # 使用 Friend model 验证数据
            friend = Friend(**friend_data)

        return jsonify(friend.dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
