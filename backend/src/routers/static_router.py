from flask import Blueprint, send_from_directory
import os

bp = Blueprint('static', __name__)

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
static_dir = os.path.join(current_dir, 'static', 'chat-app')

@bp.route('/')
def serve_index():
    return send_from_directory(static_dir, 'index.html')

@bp.route('/<path:path>')
def serve_static(path):
    return send_from_directory(static_dir, path)
