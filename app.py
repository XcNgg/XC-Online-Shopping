from flask import Flask
from flask import render_template,request,redirect,url_for,g,session
from flask_migrate import Migrate
from extension import db,mail
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

@app.before_request
def before_requests():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = XcOSUser.query.get(user_id)
            # setattr给什么属性绑定什么变量
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # 此时的g是全局变量
            setattr(g,'user',user) # 等于  g.user= user
        except:
            g.user = None # 等于 setattr(g,'user',None)


@app.context_processor
# 当渲染的所有网站都会执行以下的代码
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
