#coding=utf8
import os
import platform

path = os.path
basedir = path.abspath(path.dirname(__file__))
cursystem = platform.system()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'whats your name' # 秘钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AUTUMNLIFE_MAIL_SUBJECT_PREFIX = '[AutumnLife]' # 邮件名称抬头
    AUTUMNLIFE_MAIL_SENDER = 'Hoster Wang <' + str(os.environ.get('MAIL_USERNAME')) + '>' # 邮件发送人
    AUTUMNLIFE_ADMIN = os.environ.get('AUTUMNLIFE_ADMIN')
    AUTUMNLIFE_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                cursystem is 'Windows' and 'sqlite:///' + os.path.join(basedir, \
                'dbs\\autumnpy.db') or 'sqlite:////' + os.path.join(basedir, 'dbs/autumnpy.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'dbs\\data-test.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'dbs\\data.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}