# coding=utf8

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp
from ..models import User, Role

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('submit')


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'简介')
    submit = SubmitField(u'提交')


# 管理员的资料编辑表单
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username',
                           validators=[Required(), Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名至少包含一个字母、数字、'
                                              '小数点或下划线')])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)  # 把字段的值转换为整数
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('简介')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)\
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    # http://blog.csdn.net/hyman_c/article/details/53998812
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册！')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被注册使用!')