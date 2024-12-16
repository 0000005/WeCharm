from flask import Flask
from flask_cors import CORS
from routers.llm import bp as llm_bp
from routers.setting import bp as setting_bp
from routers.friend import bp as friend_bp

app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许跨域请求

# 注册路由（添加 /api 前缀）
app.register_blueprint(llm_bp, url_prefix="/api")
app.register_blueprint(setting_bp, url_prefix="/api/setting")
app.register_blueprint(friend_bp, url_prefix="/api/friend")


@app.route("/")
def hello():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
