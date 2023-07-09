"""
models.py 数据库模型文件
flask db init
flask db migrate
flask db upgrade
"""
from extension import db

class XcOSUser(db.Model):
    # 用户表 (User table)
    __tablename__ = 'XcOS_user'
    # 设置表名为 'XcOS_user' (Set table name as 'XcOS_user')

    id = db.Column(db.Integer, primary_key=True)
    # 用户ID (User ID)
    username = db.Column(db.String(255), nullable=False)
    # 用户名 (Username)
    password = db.Column(db.String(255), nullable=False)
    # 密码 (Password)
    email = db.Column(db.String(255), nullable=False)
    # 邮箱 (Email)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)


class XcOSProduct(db.Model):
    # 产品表 (Product table)
    __tablename__ = 'XcOS_product'
    # 设置表名为 'XcOS_product' (Set table name as 'XcOS_product')

    id = db.Column(db.Integer, primary_key=True)
    # 产品ID (Product ID)
    name = db.Column(db.String(255), nullable=False)
    # 产品名称 (Product name)
    description = db.Column(db.Text)
    # 产品描述 (Product description)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 产品价格 (Product price)
    image = db.Column(db.String(255))
    # 产品图片 (Product image)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)


class XcOSCart(db.Model):
    # 购物车表 (Cart table)
    __tablename__ = 'XcOS_cart'
    # 设置表名为 'XcOS_cart' (Set table name as 'XcOS_cart')

    id = db.Column(db.Integer, primary_key=True)
    # 购物车ID (Cart ID)
    user_id = db.Column(db.Integer, db.ForeignKey('XcOS_user.id'), nullable=False)
    # 用户ID，外键关联到'XcOS_user'表中的'id'字段 (User ID, foreign key reference to 'id' field in 'XcOS_user' table)
    product_id = db.Column(db.Integer, db.ForeignKey('XcOS_product.id'), nullable=False)
    # 产品ID，外键关联到'XcOS_product'表中的'id'字段 (Product ID, foreign key reference to 'id' field in 'XcOS_product' table)
    quantity = db.Column(db.Integer, nullable=False)
    # 购买数量 (Purchase quantity)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)


class XcOSOrder(db.Model):
    # 订单表 (Order table)
    __tablename__ = 'XcOS_order'
    # 设置表名为 'XcOS_order' (Set table name as 'XcOS_order')

    id = db.Column(db.Integer, primary_key=True)
    # 订单ID (Order ID)
    user_id = db.Column(db.Integer, db.ForeignKey('XcOS_user.id'), nullable=False)
    # 用户ID，外键关联到'XcOS_user'表中的'id'字段 (User ID, foreign key reference to 'id' field in 'XcOs_user' table)
    total_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 订单总金额 (Total amount of the order)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)


class XcOsOrderDetail(db.Model):
    # 订单详情表 (Order detail table)
    __tablename__ = 'XcOS_order_detail'
    # 设置表名为 'XcOs_order_detail' (Set table name as 'XcOs_order_detail')

    id = db.Column(db.Integer, primary_key=True)
    # 订单详情ID (Order detail ID)
    order_id = db.Column(db.Integer, db.ForeignKey('XcOS_order.id'), nullable=False)
    # 订单ID，外键关联到'XcOS_order'表中的'id'字段 (Order ID, foreign key reference to 'id' field in 'XcOS_order' table)
    product_id = db.Column(db.Integer, db.ForeignKey('XcOS_product.id'), nullable=False)
    # 产品ID，外键关联到'XcOS_product'表中的'id'字段 (Product ID, foreign key reference to 'id' field in 'XcOS_product' table)
    quantity = db.Column(db.Integer, nullable=False)
    # 购买数量 (Purchase quantity)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 产品价格 (Product price)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)

class XcOsEmailCaptcha(db.Model):
    # emial验证码存储模型
    __tablename__ = 'XcOS_email_captcha'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # 邮箱不为空，且唯一
    email = db.Column(db.String(100),nullable=False,unique=True)
    # 验证码不为空，且唯一
    captcha = db.Column(db.String(10),nullable=False,unique=True)
    # 验证码发送时间
    send_time = db.Column(db.Integer,nullable=False)
    # # 验证码有效时间
    valid_time = db.Column(db.Integer,nullable=False)