import flask
from flask import Blueprint, request, render_template, redirect, g

home = Blueprint('home', __name__, url_prefix='/')


@home.route('/')
def index():
    info = {
        'title': '小草Shopping-首页',
        'logo_title': '小草Shopping'
    }
    return render_template('index.html', info=info)
