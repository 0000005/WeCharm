import io
import sys
from flask import Flask
from flask_cors import CORS
import logging
import os
import sys
from routers.llm_router import bp as llm_bp
from routers.setting_router import bp as setting_bp
from routers.friend_router import bp as friend_bp
from routers.weixin_router import bp as weixin_bp
from routers.static_router import bp as static_bp

# 设置标准输出编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 确保logs目录存在
if getattr(sys, "frozen", False):
    # 如果是打包后的环境
    base_dir = os.path.dirname(os.path.dirname(sys.executable))
else:
    base_dir = os.path.dirname(os.path.dirname(__file__))

logs_dir = os.path.join(base_dir, "WeChat Copilot", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置日志
if getattr(sys, "frozen", False):
    # 打包环境下，使用基本的日志配置
    logging.basicConfig(
        filename=os.path.join(logs_dir, "backend.log"),
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
else:
    # 开发环境下，使用配置文件
    logging.config.fileConfig(
        os.path.join(os.path.dirname(__file__), "config", "logging.conf")
    )

logger = logging.getLogger("weixin_copilot")

app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许跨域请求

# 注册路由（添加 /api 前缀）
app.register_blueprint(llm_bp, url_prefix="/api/llm")
app.register_blueprint(setting_bp, url_prefix="/api/setting")
app.register_blueprint(friend_bp, url_prefix="/api/friend")
app.register_blueprint(weixin_bp, url_prefix="/api/weixin")
app.register_blueprint(static_bp, url_prefix="/chat-app")


@app.route("/")
def hello():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
