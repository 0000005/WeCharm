from flask import Blueprint, jsonify, abort

bp = Blueprint("llm", __name__, url_prefix="/llm")


@bp.route("/ping")
def ping():
    """Simple ping endpoint to test if the API is running"""
    return jsonify({"message": "pong"})


# 意图探索接口

# 智能回复接口

# 好友信息保存接口

# 系统设置保存接口
