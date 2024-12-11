from flask import Flask
from flask_cors import CORS
from routers.llm import bp as llm_bp

app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许跨域请求

# 注册测试路由
app.register_blueprint(llm_bp)


@app.route("/")
def hello():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
