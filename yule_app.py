from flask import Flask, render_template, request, session, redirect, Blueprint, jsonify
import pymongo
import uuid
import time
import markdown
import bleach
import re
import os

import dbConnecter

yule_app = Blueprint('yule_app', __name__)
yule_app.secret_key = os.getenv('SECRET_KEY')
client = pymongo.MongoClient()
db = client.reciter

'''
    集合名 yule

    name 游戏名
    hot 游戏热度
    path 游戏html文件路径
    intro 游戏介绍路径
    timef 创建时间
    creator 创建者
    
    CREATE TABLE yule (
        name VARCHAR(128), 
        hot INT, 
        path VARCHAR(256), 
        intro VARCHAR(256), 
        timef VARCHAR(64), 
        creator VARCHAR(128)
    );
'''


request_logs = {}
MAX_REQUESTS = 10  # 每分钟最多允许的请求数
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


@yule_app.before_request
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


@yule_app.route('/yule')
def yule():
    # dics = db.yule.find()
    # dics = list(dics)
    dics = dbConnecter.read_data('yule')
    dics.sort(key=lambda x: x['hot'], reverse=True)
    return render_template('yule/yule.html',
                           t_dics=dics,
                           t_theme=get_theme(),
                           t_username=session.get('username'))


@yule_app.route('/intro', methods=['GET'])
def intro():
    name = request.args.get('name')
    # dic = db.yule.find_one({'id': id})
    dic = dbConnecter.read_data('yule', 'name', name)[0]
    intro_path = dic['intro']
    print(intro_path)
    with open(intro_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = markdown.markdown(content, extensions=['markdown.extensions.fenced_code',
                                                     'markdown.extensions.codehilite',
                                                     'markdown.extensions.extra',
                                                     'markdown.extensions.toc',
                                                     'markdown.extensions.tables'])
    return render_template('yule/intro.html',
                           t_name=dic['name'],
                           t_intro=content,
                           t_username=session.get('username'),
                           t_theme=get_theme(),
                           t_timef=dic['timef'],
                           t_creator=dic['creator'],
                           t_hot=dic['hot'])

@yule_app.route('/games', methods=['GET'])
def games():
    if session.get('username') == None:
        return redirect('/login')
    name = request.args.get('name')
    r = dbConnecter.read_data('yule', 'name', name)[0]
    # r = db.yule.find_one({'id': id})
    r['hot'] += 1
    # db.yule.update({'id': id}, r)
    dbConnecter.update_data('yule', 'name', name, 'hot', r['hot'])
    return render_template(r['path'])