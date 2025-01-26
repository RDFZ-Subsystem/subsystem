from flask import Flask, render_template, request, session, redirect, Blueprint
import pymongo
import time
import os
import dbConnecter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from user_app import user_app
from recite_app import recite_app
from forum_app import forum_app
from yule_app import yule_app


app = Flask(__name__)
app.secret_key = '123'
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
    default_limits=["2 per second"]  # 应用默认速率限制（全局）
)

limiter.limit('2 per second')(user_app)
limiter.limit('2 per second')(recite_app)
limiter.limit('2 per second')(forum_app)
limiter.limit('2 per second')(yule_app)


def get_theme():
    theme = session.get('theme')
    if theme == None:
        theme = 'white'
    return theme


@app.route('/')
@limiter.limit('2 per second')
def main():
    # username = session.get('username')
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
    return render_template('main/main.html',
                           )


if __name__ == '__main__':
    app.run(debug=True, port=5050)