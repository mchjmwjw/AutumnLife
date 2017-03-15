#coding=utf8
from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required
from ..models import User
from .forms import LoginForm, RegistrationForm

# 登录页面
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()  # 查找出邮箱名对应的用户
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        
        flash('Invalid username or password.')  # 输入的用户名或密码不合法，提示消息
    
    return render_template('auth/login.html', form=form)

@auth.route('/secret')
@login_required     # 未认证用户访问该路由，将会被拦截
def secret():
    return render_template('auth/secret.html')

@auth.route('auth/logout')
@login_required
def logout():
    logout_user()
    flash(u'用户已注销!')
    return redirect(url_for('main.index'))

@auth.route('auth/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    user = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        flash(u'正在登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)