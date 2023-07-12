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
    balance = db.Column(db.DECIMAL(10, 2), nullable=False, default=0.00)
    # 用户余额 (User balance)
    addresses = db.relationship('XcOSAddress', backref='user', lazy=True)
    # 用户与收货地址的关联关系 (User-address relationship)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)
    # def __repr__(self):
    #     return f"<XcOSUser  {self.username } {self.email} {self.balance}>"


class XcOSAddress(db.Model):
    # 收货地址表 (Address table)
    __tablename__ = 'XcOS_address'
    # 设置表名为 'XcOS_address' (Set table name as 'XcOS_address')
    id = db.Column(db.Integer, primary_key=True)
    # 地址ID (Address ID)
    user_id = db.Column(db.Integer, db.ForeignKey('XcOS_user.id'), nullable=False)
    # 用户ID，外键关联到'XcOS_user'表中的'id'字段 (User ID, foreign key reference to 'id' field in 'XcOS_user' table)
    state = db.Column(db.String(100), nullable=False)
    # 省/州 (State)
    city = db.Column(db.String(100), nullable=False)
    # 城市 (City)
    detailed_address = db.Column(db.String(255), nullable=False)
    # 如街道地址、门牌号 公寓号、楼层等
    postal_code = db.Column(db.String(20), nullable=True)
    # 邮政编码 (Postal code)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)
    # def __repr__(self):
    #     return f"<XcOSAddress {self.id } {self.user_id } {self.state } {self.city} {self.detailed_address} {self.postal_code}>"

class XcOsEmailCaptcha(db.Model):
    # emial验证码存储模型
    __tablename__ = 'XcOS_email_captcha'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    # 邮箱不为空，且唯一
    captcha = db.Column(db.String(10),nullable=False,unique=True)
    # 验证码不为空，且唯一
    send_time = db.Column(db.Integer,nullable=False)
    # 验证码发送时间
    valid_time = db.Column(db.Integer,nullable=False)
    # # 验证码有效时间
    # def __repr__(self):
    #     return f"<XcOSAddress {self.email} {self.captcha} {self.send_time} {self.valid_time}>"

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
    product_type = db.Column(db.String(50), nullable=False)
    # 产品类型 (Product type)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)
    # def __repr__(self):
    #     return f"<XcOSProduct {self.name} {self.description} {self.product_type} {self.image} {self.product_type} >"

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
    # def __repr__(self):
    #     return f"<XcOSCart {self.id} {self.user_id} {self.product_id} {self.quantity} >"

class XcOsOrderDetail(db.Model):
    # 订单详情表 (Order detail table)
    __tablename__ = 'XcOS_order_detail'
    # 设置表名为 'XcOS_order_detail' (Set table name as 'XcOS_order_detail')
    id = db.Column(db.Integer, primary_key=True)
    # 订单详情ID (Order detail ID)
    product_id = db.Column(db.Integer, db.ForeignKey('XcOS_product.id'), nullable=False)
    # 产品ID，外键关联到'XcOS_product'表中的'id'字段 (Product ID, foreign key reference to 'id' field in 'XcOS_product' table)
    quantity = db.Column(db.Integer, nullable=False)
    # 购买数量 (Purchase quantity)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 产品价格 (Product price)
    total_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 订单总金额 (Total amount of the order)
    address_id = db.Column(db.Integer, db.ForeignKey('XcOS_address.id'), nullable=False)
    # 收货地址ID，外键关联到'XcOS_address'表中的'id'字段 (Address ID, foreign key reference to 'id' field in 'XcOS_address' table)
    status = db.Column(db.String(50), nullable=False)
    # 订单状态 (Order status)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)
    # def __repr__(self):
    #     return f"<XcOSOrderDetail {self.id} {self.product_id} {self.quantity} {self.total_amount} {self.address_id} {self.status} >"

class XcOSAdmin(db.Model):
    # 管理员表 (Admin table)
    __tablename__ = 'XcOS_admin'
    # 设置表名为 'XcOS_admin' (Set table name as 'XcOS_admin')

    id = db.Column(db.Integer, primary_key=True)
    # 管理员ID (Admin ID)
    username = db.Column(db.String(255), nullable=False)
    # 管理员用户名 (Admin username)
    password = db.Column(db.String(255), nullable=False)
    # 管理员密码 (Admin password)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 创建时间 (Creation timestamp)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # 更新时间 (Update timestamp)
    # def __repr__(self):
    #     return f"<XcOSAdmin {self.username}>"


class XcOSSignIn(db.Model):
    # 签到表 (Sign-in table)
    __tablename__ = 'XcOS_sign_in'
    # 设置表名为 'XcOS_sign_in' (Set table name as 'XcOS_sign_in')
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # 签到记录ID (Sign-in record ID)
    user_id = db.Column(db.Integer, db.ForeignKey('XcOS_user.id'), nullable=False)
    # 用户ID，外键关联到'XcOS_user'表中的'id'字段 (User ID, foreign key reference to 'id' field in 'XcOS_user' table)
    sign_in_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    # 签到时间 (Sign-in time)
    amount = db.Column(db.DECIMAL(5, 2), nullable=False)
    # 签到金额 (Sign-in amount)
    # def __repr__(self):
    #    return f"<XcOSSignIn {self.id}>"


# class XcOSOrder(db.Model):
#     # 订单表 (Order table)
#     __tablename__ = 'XcOS_order'
#     # 设置表名为 'XcOS_order' (Set table name as 'XcOS_order')
#     id = db.Column(db.Integer, primary_key=True)
#     # 订单ID (Order ID)
#     user_id = db.Column(db.Integer, db.ForeignKey('XcOS_user.id'), nullable=False)
#     # 用户ID，外键关联到'XcOS_user'表中的'id'字段 (User ID, foreign key reference to 'id' field in 'XcOs_user' table)
#     created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
#     # 创建时间 (Creation timestamp)
#     updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
#                            onupdate=db.func.current_timestamp())
#     # 更新时间 (Update timestamp)