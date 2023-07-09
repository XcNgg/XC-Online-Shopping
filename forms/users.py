"""
forms.users.py
    用户处理的 表单文件
"""
import wtforms
from wtforms.validators import Length, email, regexp, EqualTo, InputRequired


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

