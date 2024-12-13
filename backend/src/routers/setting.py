from flask import Blueprint, jsonify, request
import json
import os

bp = Blueprint("setting", __name__)

# TODO 好友信息保存接口


@bp.route("/setting/save", methods=["POST"])
def save_settings():
    """Save application settings to setting.json file"""
    try:
        settings_data = request.get_json()

        # 确保settings.json文件所在的目录存在
        settings_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(settings_dir, exist_ok=True)

        # 保存设置到文件
        settings_file = os.path.join(settings_dir, "setting.json")
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=2)

        return jsonify({"message": "Settings saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/setting/load", methods=["GET"])
def load_settings():
    """Load application settings from setting.json file"""
    try:
        settings_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        settings_file = os.path.join(settings_dir, "setting.json")

        # 如果文件不存在，返回空配置
        if not os.path.exists(settings_file):
            return jsonify({}), 200

        # 读取设置文件
        with open(settings_file, "r", encoding="utf-8") as f:
            settings_data = json.load(f)

        return jsonify(settings_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
