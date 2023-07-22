import flask
from flask import Blueprint, request, render_template, redirect, g, jsonify, url_for, session, make_response
from flask_mail import Message
from extension import db
import random
import string
import time
from models import XcOsEmailCaptcha, XcOSUser, XcOSSignIn,XcOSProduct
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
from sqlalchemy import or_
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
    data_length = XcOSProduct.query.count()
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
    # 使用 or_ 运算符组合多个过滤条件
    filter_conditions = or_(XcOSProduct.name.like(f'{keyword}%'),
                            XcOSProduct.product_type == product_type)

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


@products.route('/productinfo', methods=['get'])
def product_info():
    id = request.args.get('id')
    return {'code':200,'data':id}