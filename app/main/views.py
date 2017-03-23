#coding=utf8
from flask import render_template
from . import main
import os
from flask import send_from_directory
import app

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/icon')

# 用户资料
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)