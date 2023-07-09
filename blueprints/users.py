import flask
from flask import Blueprint,request,render_template,redirect,g

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form =request.form
        return f'{form}'



@users.route('/regist',methods=['GET',"POST"])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        form =request.form
        return f'{form}'
