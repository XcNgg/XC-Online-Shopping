"""
forms.users_form.py
    用户处理的 表单文件
"""
import wtforms
from wtforms.validators import Length, email, regexp, EqualTo, InputRequired
import time
from models import XcOSUser,XcOsEmailCaptcha


# 注册表单
class RegistForm(wtforms.Form):
    """
        以下属性均来自于前端 form 的name 值
    """
    # 用户名验证
    username = wtforms.StringField(validators=[Length(min=3,max=10)])
    # 邮箱验证
    email =wtforms.StringField(validators=[email()])
    # 密码验证
    password = wtforms.StringField(validators=[Length(min=8,max=20)])
    # # 确认密码验证
    password_confirm =wtforms.StringField(validators=[EqualTo('password')])
    # # 验证码
    captcha = wtforms.StringField(validators=[Length(min=6,max=6)])

    # 定一个验证方法，验证码是否存在问题
    def validate_captcha(self,filed):
        captcha = filed.data
        email = self.email.data
        captcha_model = XcOsEmailCaptcha.query.filter_by(email = email).first()
        # 获取当前时间戳
        now_time = int(time.time())
        if now_time < captcha_model.valid_time:
            if not captcha_model or  captcha_model.captcha.lower() != captcha.lower():
                # print("邮箱验证码错误！")
                raise wtforms.ValidationError("邮箱验证码错误！")
        else:
            # print("邮箱验证码超时!")
            raise wtforms.ValidationError("邮箱验证码超时!")

    # 定义一个邮箱验证码方法
    def validate_email(self,filed):
        email = filed.data
        user_model = XcOSUser.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('当前邮箱已经存在！')



# 登录验证表单
class LoginForm(wtforms.Form):
    # 邮箱验证
    email = wtforms.StringField(validators=[email(Length(min=3,max=10,message='邮箱格式错误！'))])
    # 密码验证
    password = wtforms.StringField(validators=[Length(min=8, max=20,message='密码格式错误！')])

    # 判断该邮箱是否存在
    def validate_email(self, filed):
        email = filed.data
        user_model = XcOSUser.query.filter_by(email=email).first()
        if not user_model:
            raise wtforms.ValidationError('邮箱不存在!')


