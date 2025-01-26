from flask import Flask, render_template, request, session, redirect, Blueprint, jsonify
import pymongo
import time
import os
import markdown
import dbConnecter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from user_app import user_app
from recite_app import recite_app
from forum_app import forum_app
from yule_app import yule_app


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(user_app)
app.register_blueprint(recite_app)
app.register_blueprint(forum_app)
app.register_blueprint(yule_app)

# client = pymongo.MongoClient()
# db = client.reciter

# 初始化 Limiter
limiter = Limiter(
    get_remote_address,  # 使用客户端 IP 地址进行速率限制
    app=app,  # 绑定到应用
    default_limits=["20 per minute"]  # 应用默认速率限制（全局）
)

limiter.limit('10 per minute')(user_app)
limiter.limit('10 per minute')(recite_app)
limiter.limit('10 per minute')(forum_app)
limiter.limit('10 per minute')(yule_app)

request_logs = {}
MAX_REQUESTS = 20  # 每分钟最多允许的请求数
TIME_WINDOW = 60  # 时间窗口（秒）


def log_request(fingerprint):
    """记录访问行为"""
    current_time = time.time()
    if fingerprint not in request_logs:
        request_logs[fingerprint] = []
    request_logs[fingerprint].append(current_time)

    # 保留时间窗口内的请求记录
    request_logs[fingerprint] = [t for t in request_logs[fingerprint] if current_time - t <= TIME_WINDOW]

    # 判断是否超过阈值
    if len(request_logs[fingerprint]) > MAX_REQUESTS:
        return True  # 超过限制，标记为可疑
    return False


@app.before_request
def detect_bot():
    # 根据 User-Agent + IP 生成设备指纹
    user_agent = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    fingerprint = f"{ip}_{user_agent}"  # 简单生成指纹，实际可以用更复杂的方法

    # 检查行为是否异常
    if log_request(fingerprint):
        return jsonify({"error": "Too many requests, potential bot detected."}), 429


def get_theme():
    theme = session.get('theme')
    if theme == None:
        theme = 'white'
    return theme


@app.route('/')
@limiter.limit('10 per minute')
def main():
    username = session.get('username')
    # s = 0
    # e = 5
    # lists = list(db.lists.find())
    # top = list(db.articles.find({'top': True}))
    # rec = list(db.articles.find({'top': False}))
    # lists.sort(key=lambda x: x['timef'], reverse=True)
    # rec.sort(key=lambda x: x['timef'], reverse=True)
    # top.sort(key=lambda x: x['timef'], reverse=True)
    # lists = lists[s: e]
    # rec = rec[s: e]
    with open('static/md/main/main.md', 'r', encoding='utf-8') as file:
        content = file.read()

    content = markdown.markdown(content, extensions=['markdown.extensions.fenced_code',
                                                     'markdown.extensions.codehilite',
                                                     'markdown.extensions.extra',
                                                     'markdown.extensions.toc',
                                                     'markdown.extensions.tables'])
    return render_template('main/main.html',
                           t_content=content,
                           t_username=username,
                           t_theme=get_theme())


if __name__ == '__main__':
    app.run(debug=True, port=5050)