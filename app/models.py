#coding=utf8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sex = db.Column(db.Integer, default = 1)
    password_hash = db.Column(db.String(128))

    @property
    def password(self): # 试图读取password的值将会报错
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, 'pbkdf2:sha256')

    def verify_password(self, password):    # 返回True表示密码正确
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username