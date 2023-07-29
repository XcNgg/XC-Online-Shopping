"""
config.py
    配置文件,配置app信息
"""

"""
    MySQL配置
    HOSTNAME="192.168.200.140"
    PORT=3306
    DATABASE="question_project"
    PASSWORD="zYjWbRHzD7RGYh7y"
    DB_URI="mysql+pymysql://root:{}@{}:{}/{}?charset=utf8".format(PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI=DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY="XcNgg_question_project_@2022"
"""

# todo MySQL配置 需要修改
MYSQLCONFIG = {
    "HOSTNAME": "127.0.0.1",
    "PORT": 3306,
    "USERNAME": "OnlineShopping",
    "PASSWORD": "OnlineShopping",
    "DATABASE": "OnlineShopping"
}

# 设置DB_URI
DB_URI = "mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8".format(**MYSQLCONFIG)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# todo 安全密钥需要修改
SECRET_KEY = "xiaocao_oline_shopping_@2023"


""" 邮箱验证配置
MAIL_SERVER : 默认为 ‘localhost’
MAIL_PORT : 默认为 25
MAIL_USE_TLS : 默认为 False
MAIL_USE_SSL : 默认为 False
MAIL_DEBUG : 默认为 app.debug
MAIL_USERNAME : 默认为 None
MAIL_PASSWORD : 默认为 None
MAIL_DEFAULT_SENDER : 默认为 None
MAIL_MAX_EMAILS : 默认为 None
MAIL_SUPPRESS_SEND : 默认为 app.testing
MAIL_ASCII_ATTACHMENTS : 默认为 False
"""
# 服务器地址
MAIL_SERVER = "smtp.qq.com"
# 端口
MAIL_PORT = 465
#
MAIL_USE_TLS = False
#
MAIL_USE_SSL = True
# 如果后续部署,需要更改为False
MAIL_DEBUG = True
# todo 邮箱发送的密钥需要修改
# 邮箱账号 STMP密钥
MAIL_USERNAME = "xcuptop@qq.com"
MAIL_PASSWORD = "necizvuaiohddjgg"
# 默认发件人
MAIL_DEFAULT_SENDER = "xcuptop@qq.com"
#
# MAIL_MAX_EMAILS =
#
# MAIL_SUPPRESS_SEND
#
# MAIL_ASCII_ATTACHMENTS


# todo 百度接口配置,需要官网申请
# https://ai.baidu.com/ai-doc/ANTIPORN/Jk3h6x8t2
# 百度接口配置
APP_ID = "28015953"
API_KEY = "YXyh7vONslNSbkXmIEL2FG2l"
SECRET_KEY ="YK40cgDdhqF70I0f7iNua8AguCMpqzA8"