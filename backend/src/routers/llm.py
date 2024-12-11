from flask import Blueprint, jsonify, abort

bp = Blueprint("llm", __name__, url_prefix="/llm")


@bp.route("/ping")
def ping():
    """Simple ping endpoint to test if the API is running"""
    return jsonify({"message": "pong"})
