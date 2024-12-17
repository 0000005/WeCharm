from flask import Blueprint, jsonify, request
import json
from utils.file_helper import get_file_path
import os
from models.setting_model import Settings

bp = Blueprint("setting", __name__)

# TODO 好友信息保存接口


@bp.route("/save", methods=["POST"])
def save_settings():
    """Save application settings to setting.json file"""
    try:
        settings_data = request.get_json()
        # 使用 Settings model 验证数据
        settings = Settings(**settings_data)

        # 保存设置到文件
        settings_file = get_file_path("setting.json")
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings.dict(), f, ensure_ascii=False, indent=2)

        return jsonify({"message": "Settings saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/load", methods=["GET"])
def load_settings():
    """Load application settings from setting.json file"""
    try:
        settings_file = get_file_path("setting.json")

        # 如果文件不存在，返回默认设置
        if not os.path.exists(settings_file):
            return jsonify(Settings().dict()), 200

        # 读取设置文件
        with open(settings_file, "r", encoding="utf-8") as f:
            settings_data = json.load(f)
            # 使用 Settings model 验证数据
            settings = Settings(**settings_data)

        return jsonify(settings.dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
