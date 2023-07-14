import flask
from flask import Blueprint, request, render_template, redirect, g, jsonify, url_for, session, make_response
from flask_mail import Message
from extension import db
import random
import string
import time
from models import XcOsEmailCaptcha, XcOSUser, XcOSSignIn
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
import re

products = Blueprint('products', __name__, url_prefix='/products')
@products.route('/', methods=['get'])
def products_home():
    return render_template('products/products.html')