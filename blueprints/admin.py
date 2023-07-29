from flask import Blueprint, request, render_template, redirect, g

admin = Blueprint('admin', __name__, url_prefix='/admin')
