from flask import Blueprint, request, render_template, redirect, g, jsonify, url_for, session, make_response
from flask_mail import Message
from extension import db
import random
import string
import time
from models import *
from extension import mail
# flask 底层的生成加密函数
from werkzeug.security import generate_password_hash
# flask 底层的解密函数
from werkzeug.security import check_password_hash
from decorators import login_required
from decimal import Decimal
from datetime import date, datetime
from sqlalchemy import func
from image_captcha import generate_image
import os
import re
from baiduImgCensor import get_img_result,convert_to_jpg
from extension import move_file

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
    integral = random.choice([1, 3, 5, 7])
    user_id = int(request.form.get('uid'))
    print(user_id)
    signin_model = XcOSSignIn.query.filter_by(user_id=user_id).first()
    if not signin_model:
        new_signin = XcOSSignIn(
            user_id=user_id,
            integral=integral,
        )
        db.session.add(new_signin)
        db.session.commit()
        user_model = XcOSUser.query.filter_by(id=user_id).first()
        user_model.integral += integral  # 更新用户积分
        db.session.commit()
        return jsonify(
            {'code': 200, 'message': "签到成功！", 'amount': f'今日随机签到积分：{integral}'}), 200
    else:
        # 判断用户今天是否签到了，如果没签到，则更新数据库并成功签到，如果签到了则返今日已经签到了
        today = date.today()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 判断用户今天是否已经完成签到
        signin_model = XcOSSignIn.query.filter_by(user_id=user_id).filter(
            func.DATE(XcOSSignIn.sign_in_time) == today).first()

        if not signin_model:
            new_signin = XcOSSignIn(
                user_id=user_id,
                sign_in_time=now,
                integral=integral,
            )
            db.session.add(new_signin)
            db.session.commit()

            user_model = XcOSUser.query.filter_by(id=user_id).first()
            user_model.integral += integral
            db.session.commit()

            return jsonify(
                {'code': 200, 'message': "签到成功！", 'amount': f'今日随机签到积分：{integral}'}), 200

        else:
            return jsonify({'code': 400, 'message': "今天已经签到了！"}), 200


# 注销清除session
@users.route('/logout')
@login_required
def logout():
    session.clear()
    return jsonify({'code': 200, 'message': '注销成功！'})


"""
----------------------------------------------------------------------------------------
登录管理
----------------------------------------------------------------------------------------
"""


# todo login的界面 需要重构 js需要建立 参考 / EmailCaptcha
# 登录界面
@users.route('/login', methods=['GET'])
def login():
    session.clear()
    if request.method == 'GET':
        return render_template('users/login.html')


# 登录验证
@users.route('/CheckLogin', methods=["POST"])
def check_login():
    if request.method == 'POST':
        if session['captcha_code'].upper() != request.form.get('captcha_code').upper():
            return jsonify({'code': 400, 'message': '验证码错误'})

        user_model = XcOSUser.query.filter_by(email=request.form.get('email')).first()
        if not user_model:
            return jsonify({'code': 400, 'message': '邮箱不存在!'})

        # 获取email
        email = request.form.get('email')
        # 获取密码
        password = request.form.get('password')
        user = XcOSUser.query.filter_by(email=email).first()
        # 使用check_password_hash函数来验证密码 函数(hashpassowrd,password)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return jsonify({'code': 200, 'message': '登录成功!'})
        else:
            return jsonify({'code': 400, 'message': '邮箱与密码不匹配！'})


# 图像验证码
@users.route('/ImageCaptcha', methods=['GET'])
def get_image_captcha():
    # 生成或获取验证码图像并将其转换为base64
    captcha_code, captcha_base64 = generate_image()
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
@users.route('/ForgotPassword', methods=['GET'])
def forgot_password():
    return render_template('users/forgotPassword.html')


# 忘记密码信息验证
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
            # print(random_password)
            message_dict = {
                "title": "小草Shopping-深耕电商服务20年 重置密码",  # 邮件标题
                "username": user_model.username,  # 接收者
                "service": "重置密码",  # 发送的服务
                "code": random_password,  # 验证码
            }
            message = Message(
                recipients=[(request.form.get('email')), ],  # 收件人
                subject='【小草Shopping-深耕电商服务20年】 重置密码',  # 邮件主题
                html=render_template('emailBase.html', **message_dict),  # 邮件内容
            )
            mail.send(message)
            user_model.password = generate_password_hash(random_password)
            db.session.commit()
            return jsonify({'code': 200, 'message': '重置密码发送成功！'})
        except Exception as e:
            print(e)
            return jsonify({'code': 500, 'message': '系统错误！'}), 500


"""
----------------------------------------------------------------------------------------
注册管理
----------------------------------------------------------------------------------------
"""


# 注册接口
@users.route('/regist', methods=['GET', "POST"])
def regist():
    if request.method == 'GET':
        return render_template('users/regist.html')


# 验证注册信息
@users.route('/CheckRegist', methods=["POST"])
def check_regist():
    username = request.form.get('username')

    # 如果存在同名用户
    if XcOSUser.query.filter_by(username=username).first():
        length = random.randint(3, 8)  # 生成随机长度
        characters = string.ascii_letters + string.digits  # 包含大小写英文字母和数字的字符集
        random_name = ''.join(random.choice(characters) for _ in range(length))
        return jsonify({'code': 409, 'message': f'用户名已被使用,试试 {username}{random_name} 吧'})

    email = request.form.get('email')

    # 如果存在相同的邮箱
    has_email = XcOSUser.query.filter_by(email=email).first()
    if has_email:
        return jsonify({'code': 409, 'message': f'邮箱已被使用！'})

    captcha = request.form.get('captcha')
    print(captcha)

    email_model = XcOsEmailCaptcha.query.filter_by(email=email).first()
    # 获取当前时间戳
    now_time = int(time.time())
    if now_time < email_model.valid_time:
        if not email_model or email_model.captcha.lower() != captcha.lower():
            return jsonify({'code': 409, 'message': '验证码错误！'})
    else:
        return jsonify({'code': 409, 'message': '验证码超时！'})

    # 上述均为通过，则注册
    password = request.form.get('password')
    new_user = XcOSUser(
        username=username,
        # 密码哈希存储
        password=generate_password_hash(password),
        email=email,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'code': 200, 'message': f'注册成功！'})


# 验证并发送邮箱验证码
@users.route('/EmailCaptcha', methods=['POST'])
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

    # 如果第一行有结果，即该用户不是第一次发送
    if email_captcha_model:
        timestamp_gap = form_timestamp - email_captcha_model.send_time
        # 判断和上次发送的时间是否超过了60秒
        gap = 60
        if timestamp_gap <= gap:
            # print(f'{form_timestamp}-{email_captcha_model.send_time} = {timestamp_gap} ')
            return jsonify({
                "code": 400,
                "message": f"请等待{gap - timestamp_gap}秒再发送！Please wait {gap - timestamp_gap} seconds before sending!"
            })
        else:
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
                    html=render_template('emailBase.html', **message_dict),  # 邮件内容
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
                    "code": 400,
                    "message": f"Service Error ! {e}"
                })

    else:  # 如果第一行没有结果，即该用户是第一次发送验证码
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
                html=render_template('emailBase.html', **message_dict),  # 邮件内容
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
        "code": 200,
        "message": "Send captcha Scuccess"
    }), 200


"""
----------------------------------------------------------------------------------------
修改密码界面
----------------------------------------------------------------------------------------
"""


@users.route('/EditPassword', methods=['GET'])
@login_required
def edit_password():
    return render_template('users/editPassword.html')


# 忘记密码验证接口
@users.route('/CheckEditPassword', methods=["POST"])
@login_required
def check_edit_password():
    user_id = session['user_id']
    old_password = request.form.get('oldPassword')
    user_model = XcOSUser.query.filter_by(id=user_id).first()
    # print(user_model.password)
    if check_password_hash(user_model.password, old_password):
        user_model.password = generate_password_hash(password=request.form.get('newPassword'))
        db.session.commit()
        session.clear()
        return jsonify({'code': 200, 'message': '密码修改成功！请重新登录！'})
    else:
        return jsonify({'code': 400, "message": "原密码错误！"})


"""
----------------------------------------------------------------------------------------
个人信息界面
----------------------------------------------------------------------------------------
"""
# 个人信息界面
@users.route('/information')
@login_required
def information():
    return render_template('users/personalInformation.html')


@users.route('/checkEditInfo', methods=["POST"])
@login_required
def check_edit_info():
    user_id = session['user_id']
    edit_username = request.form.get('editUsername').replace(' ', '')
    edit_email = request.form.get('editEmail').replace(' ', '')

    pattern = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9_]+$')
    if not pattern.match(edit_username):
        return jsonify({'code': 400, 'message': '用户名只能包含中文、大小写英文字母、下划线和数字'})

    now_user = XcOSUser.query.filter_by(id=user_id).first()

    if not now_user:
        return jsonify({'code': 404, 'message': '找不到用户'})

    has_user = XcOSUser.query.filter_by(username=edit_username).first()

    if has_user and has_user.id != user_id:
        length = random.randint(3, 8)  # 生成随机长度
        characters = string.ascii_letters + string.digits  # 包含大小写英文字母和数字的字符集
        random_name = ''.join(random.choice(characters) for _ in range(length))
        return jsonify({'code': 409, 'message': f'用户名已被使用,试试 {edit_username}{random_name} 吧'})

    has_email = XcOSUser.query.filter_by(email=edit_email).first()
    if has_email and has_email.id != user_id:
        return jsonify({'code': 409, 'message': f'邮箱已被使用！'})

    if edit_username != now_user.username and edit_email != now_user.email:
        # 用户名和邮箱都被修改
        # 执行相应操作
        now_user.email = edit_email
        now_user.username = edit_username
    elif edit_username != now_user.username:
        # 只有用户名被修改
        # 执行相应操作
        now_user.username = edit_username
    elif edit_email != now_user.email:
        # 只有邮箱被修改
        # 执行相应操作
        now_user.email = edit_email
    else:
        # 没有进行任何修改
        # 执行相应操作
        return jsonify({'code': 200, 'message': '信息未修改'})

    db.session.commit()
    return jsonify({'code': 200, 'message': '修改个人信息成功'})


"""
----------------------------------------------------------------------------------------
我的出售界面
----------------------------------------------------------------------------------------
"""
@users.route('/mySale')
@login_required
def my_sale():
    return render_template('users/mySale.html')

# 获取当前商品数量 GET请求
@users.route('/GetMySale',methods=['GET'])
@login_required
def get_my_sale():
    products_list = []
    user_id = session['user_id']
    products_result = XcOSProduct.query.filter_by(seller_id=user_id).all()
    for product in products_result:
        product_dict = {
            'id': product.id,
            # 'seller_id': product.seller_id,
            'name': product.name,
            # 'simple_description': product.simple_description,
            # 'description': product.description,
            'price': str(product.price),
            'img_path': product.img_path,
            'sales': product.sales,
            'stock': product.stock,
            'product_type': product.product_type,
            'created_at': str(product.created_at),
            'updated_at': str(product.updated_at)
        }
        products_list.append(product_dict)
        # print(product_dict)
    if not products_list:
        return jsonify({'code':200,'message':"您还没有出售中的产品哦",'data':[]})
    else:
        return jsonify({'code':200,'message':f'当前在售【{len(products_list)}】件商品','data':products_list})

@users.route('/DeleteMySale',methods=['POST'])
@login_required
def delete_my_sale():
    try:
        user_id = session['user_id']
        id = request.form.get('id')
        name = request.form.get('name')
        delete_product = XcOSProduct.query.filter_by(id=id,name=name, seller_id=user_id).first()
        if delete_product:
            print(delete_product.name)
            db.session.delete(delete_product)
            db.session.commit()
            return jsonify({'code': 200, 'message': '删除成功！'})
        else:
            return jsonify({'code': 400, 'message': '未找到要删除的数据！'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code':500,'message':e.__str__()})

"""
----------------------------------------------------------------------------------------
编辑、新增出售界面
----------------------------------------------------------------------------------------
"""
# todo 编辑、新增出售界面
@users.route('/saleInfo')
@login_required
def sale_info():
    return render_template('users/saleInfo.html')


@users.route('/CheckSaleImg',methods=['POST'])
@login_required
def check_sale_img():
    logo_img = request.files['logo_img']

    logo_img.save('./static/upload/censor/' + logo_img.filename)

    img_path = './static/upload/censor/' + logo_img.filename

    # 判断图像是否不是jpg格式
    if os.path.splitext(logo_img.filename)[-1] != '.jpg':
        # 如果非jpg格式，将图像转为Jpg格式
        img_path = convert_to_jpg(logo_img.filename)

    img_result = get_img_result(img_path=img_path)

    if 'conclusion' not in img_result:
        return jsonify({'code':500,'message':'API错误！'})

    else:

        conclusion = img_result['conclusion']

        if conclusion == '不合规' or conclusion == '疑似':
            os.remove(img_path)
            return jsonify({'code': 400, 'message': F"{img_result['data'][0]['msg']}"})

        else:
            timestamp_file_name =str(time.time())+'.jpg'
            os.rename(img_path,'./static/upload/censor/'+timestamp_file_name)
            move_file('static/upload/censor/'+timestamp_file_name,'static/upload/products/')
            return jsonify({'code':200,'message':img_result,'filename':'/static/upload/products/'+timestamp_file_name})



@users.route('/CheckSaleInfo',methods=['POST'])
@login_required
def check_sale_info():
    data = request.form

    product_type_list = ['虚拟产品']
    if data.get('product_type') not in product_type_list:
        return jsonify({'code':400,'message':'添加的数据类型不被允许'})

    if len(data.get('simple_description')) > 25:
        return jsonify({'code': 400, 'message': '产品简介过长(25个字以内)'})

    if int(data.get('stock')) < 0:
        return jsonify({'code': 400, 'message': '库存有误！'})

    if float(data.get('price')) < 1.0:
        return jsonify({'code': 400, 'message': '价格有误！'})

    seller_id = session['user_id']
    name = request.form.get('name')
    simple_description = request.form.get('simple_description')
    description = request.form.get('description')
    price = request.form.get('price')
    stock = request.form.get('stock')
    product_type = request.form.get('product_type')
    img_path = request.form.get('img_path')
    # 创建 XcOSProduct 实例
    product = XcOSProduct(name=name,seller_id=seller_id, simple_description=simple_description, description=description,
                          price=price, stock=stock, product_type=product_type, img_path=img_path)

    # 将实例添加到数据库
    db.session.add(product)
    db.session.commit()



    return jsonify({'code':200,'message':'over','data':data})
