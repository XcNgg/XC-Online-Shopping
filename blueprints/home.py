from flask import Blueprint, request, render_template, redirect, g
from extension import db
from models import XcOSProduct

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
        .filter_by(status=1, approval_status=1)
        .order_by(XcOSProduct.sales.desc())
        .limit(8)
    )


    return render_template('index.html', info=info,top_products=top_products)
