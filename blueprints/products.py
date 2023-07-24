import flask
from flask import Blueprint, request, render_template, redirect, g, jsonify, url_for, session, make_response
from flask_mail import Message
from extension import db
import random
import string
import time
from models import XcOsEmailCaptcha, XcOSUser, XcOSSignIn,XcOSProduct,XcOsOrderDetail
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
from sqlalchemy import or_,and_
import re


products = Blueprint('products', __name__, url_prefix='/products')

"""
---------------------------------------------------------------------------------------------
产品界面首页
---------------------------------------------------------------------------------------------
"""
# 产品界面
@products.route('/', methods=['get'])
def products_home():
    data_length = XcOSProduct.query.filter_by(approval_status=1).count()
    pages = data_length // 12
    if data_length % 12 != 0:
        pages += 1
    pages = list(range(1,pages+1))

    return render_template('products/products.html',pages=pages,)

@products.route('/getproduct', methods=['get'])
def get_product():
    keyword = request.args.get('keyword','')
    page = int(request.args.get('page', 1))
    product_type = request.args.get('type', '虚拟产品')
    items_per_page = 12

    products_list = []
    # 使用 and_ 运算符组合多个过滤条件
    filter_conditions = and_(
        or_(
            XcOSProduct.name.like(f'%{keyword}%'),
            XcOSProduct.simple_description.like(f'%{keyword}%'),
        ),
            XcOSProduct.product_type == product_type,
            XcOSProduct.approval_status == 1
    )

    products_model = XcOSProduct.query.filter(filter_conditions).order_by(XcOSProduct.sales.desc()).paginate(page=page, per_page=items_per_page)

    for product in products_model:
        product_dict = {
            'id': product.id,
            # 'seller_id': product.seller_id,
            'name': product.name,
            'simple_description': product.simple_description,
            # 'description': product.description,
            'price': str(product.price),
            'img_src': product.img_src,
            'sales': product.sales,
            'stock': product.stock,
            'product_type': product.product_type,
            # 'status': product.status,
            # 'approval_status': product.approval_status,
            # 'approval_info': product.approval_info,
            # 'created_at': str(product.created_at),
            # 'updated_at': str(product.updated_at)
        }
        products_list.append(product_dict)

    return jsonify(
        {
            'code':200,
            'data':products_list
        }
    )


@products.route('/productinfo', methods=['GET'])
@login_required
def product_info():
    id = request.args.get('id')
    product_model = XcOSProduct.query.filter_by(id=id).first()
    return render_template('products/productinfo.html',products=product_model)


@products.route('/AddOrders',methods=['POST'])
@login_required
def add_orders():
    user_id = session['user_id']
    if not user_id:
        return jsonify({'code':302,'message':'请先登录!'})

    numbers = int(request.form.get('buyNumber'))
    product_id = int(request.form.get('productid'))


    # 买家 数据库
    buyer_user = XcOSUser.query.filter_by(id=user_id).first()
    buyer_user_balance = buyer_user.balance
    # 产品数据库
    product = XcOSProduct.query.filter_by(id=product_id).first()
    product_price = product.price

    if user_id == product.seller_id:
        return jsonify({'code':403,'message':f'不能购买自己出售的商品'})

    # 买家余额计算
    buyer_user_result_balance = buyer_user_balance - product_price * Decimal(numbers)

    if buyer_user_result_balance < Decimal(0):
        return jsonify({'code':403,'message':f'余额不足！总价￥:{ product_price * Decimal(numbers)} | 余额：￥{buyer_user_balance}'})
    # 库存计算
    if product.stock- numbers < 0:
        return jsonify({'code': 403, 'message': f'库存不足！当前库存：{product.stock}'})

    # 产品的库存和销量变更
    product.stock = product.stock - numbers
    product.sales = product.sales + numbers

    # 如果库存为0，则自动为备货中
    if product.stock == 0:
        product.status =0

    db.session.commit()

    order_id = 0
    for n in range(1,numbers+1):
        # 用户余额变更
        buyer_user.balance = buyer_user.balance - product_price
        seller_user = XcOSUser.query.filter_by(id=product.seller_id).first()
        seller_user.balance = seller_user.balance + product_price
        # 余额变化
        new_orders = XcOsOrderDetail(
            product_id =product_id,
            seller_id=product.seller_id,
            buyer_id = user_id,
            price = product.price,
            status=1,
            buyer_balance = buyer_user.balance,
            seller_balance= seller_user.balance,
        )
        db.session.add(new_orders)
        db.session.commit()
        db.session.refresh(new_orders)
        order_id = new_orders.id

    return jsonify({'code':200,'message':f'下单成功！当前余额：￥{ buyer_user_result_balance}','order_id':order_id})

