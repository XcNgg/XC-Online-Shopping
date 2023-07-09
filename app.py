from flask import Flask
from flask import render_template,request,redirect,url_for,g,session
from flask_migrate import Migrate
from project_extension import db,mail
from blueprints import users_bp,admin_bp,home_bp
from models import XcOSUser

app = Flask(__name__)

# 配置文件来自config.py
app.config.from_object('config')
# 将db绑定在app上
db.init_app(app)
# 将mail绑定在app上
mail.init_app(app)

# 注册蓝图
app.register_blueprint(users_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(home_bp)

# ORM映射
migrate = Migrate(app, db)





if __name__ == '__main__':
    app.run()
