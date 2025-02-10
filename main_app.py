from flask import Flask, render_template, session, request, abort
import os
import markdown

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

CLOUDFLARE_IPS = {
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22",
    "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
    "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22",
    "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
}

@app.before_request
def block_non_cloudflare():
    user_ip = request.headers.get("CF-Connecting-IP", request.remote_addr)
    if not any(user_ip.startswith(ip.split('/')[0]) for ip in CLOUDFLARE_IPS):
        abort(403)

def get_theme():
    theme = session.get('theme')
    if theme == None:
        theme = 'white'
    return theme


@app.route('/')
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