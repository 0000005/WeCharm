from flask import Flask
from flask_cors import CORS
import logging.config
import os
from routers.llm_router import bp as llm_bp
from routers.setting_router import bp as setting_bp
from routers.friend_router import bp as friend_bp
from routers.weixin_router import bp as weixin_bp
from routers.static_router import bp as static_bp

# 确保logs目录存在
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置日志
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'config', 'logging.conf'))
logger = logging.getLogger('weixin_copilot')

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
