#coding=utf8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin   # 管理用户认证系统，认证状态
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import *
import hashlib


# 角色
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer) # 位标志，每一位都表示一种权限

    def __repr__(self):
        return '<Role %r>' % self.name
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLE, True),   # (权限, 是否默认)
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLE |
                          Permission.MODERATE_COMMENTS, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


# 用户资料
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sex = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64)) # 所在地
    about_me = db.Column(db.Text()) # 自我介绍
    member_since = db.Column(db.DateTime(),  default=datetime.utcnow) # 注册日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow) # 最后访问日期
    #  db.Column() 的 default 参数可以接受函数作为默认值

    @property
    def password(self):     # 试图读取password的值将会报错
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, 'pbkdf2:sha256')

    def verify_password(self, password):    # 返回True表示密码正确
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})    # 生成令牌 expiration过期时间(秒)

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)   # 返回 {'confirm': self.id}
        except:
            return False
        if data.get('confirm') != self.id:  # 验证失败
            return False
        self.confirmed = True   # 验证成功
        db.session.add(self)    # 添加用户
        return True
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)    # 调用父类的构造方法
        if self.role is None:
            if self.email == current_app.config['AUTUMNLIFE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()  # 管理员角色
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()  # 非管理员角色
    
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # 头像
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hhash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hhash}?s={size}&d={default}&r={rating}'.format(
            url=url, hhash=hhash, size=size, default=default, rating=rating
        )

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


@login_manager.user_loader
def load_user(user_id):         # 加载用户的回调函数
    return User.query.get(int(user_id))


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLE = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
    
login_manager.anonymous_user = AnonymousUser
