#coding=utf8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin   # 管理用户认证系统，认证状态
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sex = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    
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

@login_manager.user_loader
def load_user(user_id):         # 加载用户的回调函数
    return User.query.get(int(user_id))