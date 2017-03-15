#coding=utf8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'自动登录')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
    email = StringField('Email', validators=[
        Required(), Length(1, 64), Email()])
    
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能由字母、数字、下划线组成，第一位必须是字母')
    ])
    
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=
                            '两次输入的密码必须相同！')
    ])
    
    password2 = PasswordField(u'请再一次输入密码', validators=[Required()])
    
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')