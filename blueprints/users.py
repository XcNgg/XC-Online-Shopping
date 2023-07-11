import flask
from flask import Blueprint,request,render_template,redirect,g,jsonify,url_for,session,make_response
from flask_mail import Message
from extension import db
import random
import string
from forms import RegistForm,LoginForm
import time
from models import XcOsEmailCaptcha,XcOSUser,XcOSSignIn
from extension import mail
# flask 底层的生成加密函数
from werkzeug.security import generate_password_hash
# flask 底层的解密函数
from werkzeug.security import check_password_hash
from decorators import login_required
from decimal import Decimal
from datetime import date,datetime
from sqlalchemy import func
from image_captcha import generate_image



users = Blueprint('users', __name__, url_prefix='/users')

"""
----------------------------------------------------------------------------------------
全局操作
----------------------------------------------------------------------------------------
"""
# 签到验证
@users.route('/SignIn', methods=['POST'])
@login_required
def signin():
    amount = random.choice([0.50, 1.00,1.50,2.00])
    user_id = int(request.form.get('uid'))
    print(user_id)
    signin_model = XcOSSignIn.query.filter_by(user_id=user_id).first()
    if not signin_model:
        new_signin = XcOSSignIn(
            user_id=user_id,
            amount=amount,
        )
        db.session.add(new_signin)
        db.session.commit()
        user_model = XcOSUser.query.filter_by(id=user_id).first()
        user_model.balance += Decimal(amount)  # 更新用户余额
        db.session.commit()
        return jsonify({'code': 200, 'message': "签到成功！Sign in Success!",'amount':f'今日随机签到金额：￥{amount}'}), 200
    else:
        #判断用户今天是否签到了，如果没签到，则更新数据库并成功签到，如果签到了则返今日已经签到了
        today = date.today()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 判断用户今天是否已经完成签到
        signin_model = XcOSSignIn.query.filter_by(user_id=user_id).filter(
            func.DATE(XcOSSignIn.sign_in_time) == today).first()

        if not signin_model:
            new_signin = XcOSSignIn(
                user_id=user_id,
                sign_in_time=now,
                amount=amount,
            )
            db.session.add(new_signin)
            db.session.commit()

            user_model = XcOSUser.query.filter_by(id=user_id).first()
            user_model.balance += Decimal(amount)
            db.session.commit()

            return jsonify({'code': 200, 'message': "签到成功！Sign in Success!",'amount':f'今日随机签到金额：￥{amount}'}), 200
        else:
            return jsonify({'code': 400, 'message': "今日已经签到了！Already signed in today!"}), 200


# 注销清除session
@users.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')

"""
----------------------------------------------------------------------------------------
登录管理
----------------------------------------------------------------------------------------
"""

# todo login的界面 需要重构 js需要建立 参考 / EmailCaptcha
# 登录界面
@users.route('/login',methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

@users.route('/CheckLogin',methods=["POST"])
def check_login():
    if request.method == 'POST':
        # print(session['captcha_code'].upper())
        # print(request.form.get('captcha_code').upper())
        if session['captcha_code'].upper() != request.form.get('captcha_code').upper():
            return jsonify({'code': 400, 'message': '验证码错误'})

        user_model = XcOSUser.query.filter_by(email=request.form.get('email')).first()
        if not user_model:
            return jsonify({'code': 400, 'message': '邮箱不存在!'})

        else:
            form = LoginForm(request.form)
            if form.validate():
                # 获取email
                email = form.email.data
                # 获取密码
                password = form.password.data
                user = XcOSUser.query.filter_by(email=email).first()
                # 使用check_password_hash函数来验证密码 函数(hashpassowrd,password)
                if user and check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    return jsonify({'code': 200, 'message': '登录成功!'})
                    # return redirect('/')
                else:
                    return jsonify({'code': 400, 'message': '邮箱密码不匹配！'})
                    # return render_template('login.html', errors=['邮箱密码不匹配！'])
            else:
                errors = 'ERROR: '
                for field_name, field_errors in form.errors.items():
                    for error in field_errors:
                        print(f"{field_name}: {error}")
                        errors += f"{field_name}: {error};"
                return jsonify({'code': 400, 'message': errors})


# 图像验证码
@users.route('/ImageCaptcha', methods=['GET'])
def get_image_captcha():
    # Generate or fetch the captcha image and convert it to base64
    captcha_code,captcha_base64 = generate_image()  # Replace with your captcha image generation logic
    print(captcha_code)
    session['captcha_code'] = captcha_code
    # response = make_response(captcha_base64)
    # response.headers['Content-Type'] = 'text/plain'
    return captcha_base64


"""
----------------------------------------------------------------------------------------
忘记密码界面管理
----------------------------------------------------------------------------------------
"""
# 忘记密码界面
@users.route('/ForgotPassword',methods=['GET'])
def forgot_password():
    return render_template('forgot-password.html')


# 忘记密码验证接口
@users.route('/ResetPassword', methods=["POST"])
def reset_password():
    user_model = XcOSUser.query.filter_by(email=request.form.get('email')).first()
    if not user_model:
        return jsonify({'code': 400, 'message': '邮箱不存在!'})
    else:
        try:
            # 随机生成 10位 包含大小写英文、特殊符号、数字的字符串
            password_length = 10
            characters = string.ascii_letters + string.digits + string.punctuation
            random_password = ''.join(random.choice(characters) for _ in range(password_length))
            print(random_password)
            message_dict = {
                "title": "小草Shopping-深耕电商服务20年 重置密码",  # 邮件标题
                "username": user_model.username,  # 接收者
                "service": "重置密码",  # 发送的服务
                "code": random_password,  # 验证码
            }
            message = Message(
                recipients=[ (request.form.get('email')),], # 收件人
                subject='【小草Shopping-深耕电商服务20年】 重置密码',  # 邮件主题
                html=render_template('email-base.html', **message_dict),  # 邮件内容
            )
            mail.send(message)
            user_model.password =generate_password_hash(random_password),
            db.session.commit()
            print(user_model.password)

            return jsonify({'code': 200, 'message': '重置密码发送成功！'})
        except Exception as e:
            print(e)
            return jsonify({'code': 500, 'message': '系统错误！'}),500

"""
----------------------------------------------------------------------------------------
注册管理
----------------------------------------------------------------------------------------
"""

#注册接口
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
            return render_template('login.html', success='注册成功！')
        # 表单验证
        else:
            errors_list = []
            for field_name, field_errors in form.errors.items():
                for error in field_errors:
                    print(f"{field_name}: {error}")
                    errors_list.append(f"{field_name}: {error}")
            return render_template('regist.html', errors=errors_list)


# 发送邮箱验证码
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
                    "code":400,
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
                "code": 400,
                "message": f"Service Error ! {e}"
            })
            # 创建模型 赋值

    return jsonify({
        "code":200,
        "message":"Send captcha Scuccess"
    }),200





"""
----------------------------------------------------------------------------------------
个人信息界面
----------------------------------------------------------------------------------------
"""
# 个人信息界面
@users.route('/information')
@login_required
def information():
    return render_template('personal-information.html')