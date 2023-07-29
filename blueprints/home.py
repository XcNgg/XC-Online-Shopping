from flask import Blueprint, request, render_template, redirect, g
from extension import db
from models import XcOSProduct,XcOSNotice

home = Blueprint('home', __name__, url_prefix='/')


@home.route('/')
def index():
    info = {
        'title': '小草Shopping-首页',
        'logo_title': '小草Shopping'
    }

    # 查询并按销量降序排序，取前8个数据，同时满足 status=1 和 approval_status=1
    top_products = (
        XcOSProduct.query
        .filter_by(approval_status=1)
        .order_by(XcOSProduct.sales.desc())
        .limit(8)
    )

    notice_list =XcOSNotice.query.filter_by(show_on_homepage=1).order_by(XcOSNotice.updated_at.desc()).all()
    for notice in notice_list:
        print(notice.title,notice.content,notice.updated_at)


    return render_template('index.html',notice_list =notice_list,info=info,top_products=top_products)
