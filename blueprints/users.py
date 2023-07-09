import flask
from flask import Blueprint,request,render_template,redirect,g,jsonify,url_for,session
from flask_mail import Message
from extension import db
import random
import string
from forms import RegistForm,LoginForm
import time
from models import XcOsEmailCaptcha,XcOSUser
from extension import mail
# flask 底层的生成加密函数
from werkzeug.security import generate_password_hash
# flask 底层的解密函数
from werkzeug.security import check_password_hash


users = Blueprint('users', __name__, url_prefix='/users')



# 登录
@users.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            # 获取email
            email = form.email.data
            # 获取密码
            password = form.password.data
            user = XcOSUser.query.filter_by(email=email).first()
            # 使用check_password_hash函数来验证密码 函数(hashpassowrd,password)
            if user and check_password_hash(user.password,password):
                print(user)
                print(user.id)
                print(user.username)
                session['user_id']=user.id
                return redirect('/')
            else:
                return render_template('login.html',errors=['邮箱或密码不匹配!'])
        else:
            errors_list = []
            for field_name, field_errors in form.errors.items():
                for error in field_errors:
                    print(f"{field_name}: {error}")
                    errors_list.append(f"{field_name}: {error}")
            return render_template('login.html', errors=errors_list)






# 发送验证码
@users.route('/EmailCaptcha',methods=['POST'])
def email_captcha():

    # 读取POST请求中的表单值
    form_email = request.form.get('email')
    form_username = request.form.get('username')
    form_timestamp = int(request.form.get('timestamp'))

    user_model = XcOSUser.query.filter_by(email=form_email).first()
    if user_model:
        return jsonify({
            "code": 400,
            "message": f"当前邮箱已经存在！"
        })


    # 导入模型
    email_captcha_model = XcOsEmailCaptcha.query.filter_by(email=form_email).first()
    # 验证码随机6位
    captcha = ''.join(random.sample(string.ascii_letters + string.digits, 6))

    #如果第一行有结果，即该用户不是第一次发送
    if email_captcha_model:
        timestamp_gap = form_timestamp - email_captcha_model.send_time
        # 判断和上次发送的时间是否超过了60秒
        gap = 60
        if timestamp_gap <= gap:
            print(f'{form_timestamp}-{email_captcha_model.send_time} = {timestamp_gap} ')
            return jsonify({
                "code": 400,
                "message": f"请等待{gap - timestamp_gap}秒再发送！Please wait {gap - timestamp_gap} seconds before sending!"
            })
        else:
            try:
                message_dict={
                    "title":"小草Shopping-深耕电商服务20年 感谢您的注册！", # 邮件标题
                    "username":form_username, # 接收者
                    "service":"用户注册", # 发送的服务
                    "code":captcha, # 验证码
                }
                message= Message(
                    recipients=[form_email],# 收件人
                    subject='【小草Shopping-深耕电商服务20年】 验证码',# 邮件主题
                    html=render_template('email-base.html', **message_dict),  # 邮件内容
                )
                # 发送邮件
                mail.send(message)
                # 将验证码赋值模型
                email_captcha_model.captcha = captcha
                # 将验证码发送时间赋值模型
                email_captcha_model.send_time = int(time.time())
                # 设置超时时间
                email_captcha_model.valid_time = int(time.time() + 300)
                # 提交模型到数据库
                db.session.commit()

            except Exception as e:
                print(e)
                return jsonify({
                    "code":500,
                    "message":f"Service Error ! {e}"
                })

    else:#如果第一行没有结果，即该用户是第一次发送验证码
        try:
            message_dict = {
                "title": "小草Shopping-深耕电商服务20年 感谢您的注册！",  # 邮件标题
                "username": form_username,  # 接收者
                "service": "用户注册",  # 发送的服务
                "code": captcha,  # 验证码
            }
            message = Message(
                recipients=[form_email],  # 收件人
                subject='【小草Shopping-深耕电商服务20年】 验证码',  # 邮件主题
                html=render_template('email-base.html', **message_dict),  # 邮件内容
            )
            # 发送邮件
            mail.send(message)
            #
            email_captcha_model = XcOsEmailCaptcha()
            email_captcha_model.email = form_email
            email_captcha_model.captcha = captcha
            # 设置发送时间
            email_captcha_model.send_time = int(time.time())
            # 设置超时时间
            email_captcha_model.valid_time = int(time.time() + 300)
            # 添加模型
            db.session.add(email_captcha_model)
            # 提交模型到数据库
            db.session.commit()

        except Exception as e:
            print(e)
            return jsonify({
                "code": 500,
                "message": f"Service Error ! {e}"
            })
            # 创建模型 赋值

    return jsonify({
        "code":200,
        "message":"Send captcha Scuccess"
    })


@users.route('/regist',methods=['GET',"POST"])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    # 如果是POST请求
    else:
        form = RegistForm(request.form)
        # 表单验证
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            new_user = XcOSUser(
                username=username,
                # 密码哈希存储
                password=generate_password_hash(password),
                email=email,
            )
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html',  success='注册成功！')
        # 表单验证
        else:
            errors_list = []
            for field_name, field_errors in form.errors.items():
                for error in field_errors:
                    print(f"{field_name}: {error}")
                    errors_list.append(f"{field_name}: {error}")
            return render_template('regist.html', errors=errors_list)


# 注销清除session
@users.route('/logout')
def logout():
    session.clear()
    return render_template('login.html',  success='您已注销！')