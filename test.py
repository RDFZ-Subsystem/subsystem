# 文件路径: app.py

from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.recaptcha import RecaptchaField

# 初始化 Flask 应用
app = Flask(__name__)
app.secret_key = "your_secret_key"

# 配置 reCAPTCHA（需要在 Google Cloud 获取以下密钥）
app.config['RECAPTCHA_PUBLIC_KEY'] = 'your_recaptcha_public_key'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'your_recaptcha_private_key'

# 配置 Flask-Limiter（速率限制）
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]  # 全局限制
)

# 创建一个带有 reCAPTCHA 的表单
class CaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # 限制此路由每分钟最多访问 5 次
def index():
    form = CaptchaForm()
    if request.method == "POST":
        if form.validate_on_submit():
            return jsonify({"message": "CAPTCHA passed, form submitted successfully!"})
        return jsonify({"error": "CAPTCHA failed, please try again!"}), 400
    return render_template("index.html", form=form)


@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({"error": "Too many requests, please slow down!"}), 429


if __name__ == "__main__":
    app.run(debug=True)
