# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))
# SQL_BASE = os.environ.get('MYSQL_HOST')
SQL_BASE = 'mysql+pymysql://root:xtalpi@localhost:3306/'
DB_NAME = 'phizard'
# defines the SQL database
# DEF_SQL = SQL_BASE + 'MEncoder'
# DEF_SQL_DEBUG = SQL_BASE + 'MEncoderDEBUG'
# DEF_SQL_TEST = SQL_BASE + 'MEncoderTEST'
# SQL_BASE = 'mysql+pymysql://root:xtalpi@localhost:3306/'
DEF_SQL = SQL_BASE + 'phizard'
DEF_SQL_DEBUG = DEF_SQL
DEF_SQL_TEST = DEF_SQL


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xtalpi-beijing'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    # 定义用户密码加密salt（生产环境中应该写入环境变量）
    SECURITY_PASSWORD_SALT = os.environ.get('SALT_KEY') or 'xtalpi-beijing-is-wonderful'
    TOKEN_SALT = b''

    SKYNET_USERS_PER_PAGE = 10
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 发送邮件的相关配置
    MAIL_SERVER = "http://api.sendcloud.net/apiv2/mail/sendtemplate"
    MAIL_USE_TLS = True  # 传输层安全协议
    API_USER = 'sunnily_test_lGWzLv'  # 账号
    API_KEY = 'v2imT0CV4I9IWJfy'  # 密码
    FROMNAME = 'XtalPi'  # 前缀
    INVORKTYPE = {0: 'template_notification', 1: 'template_rpc'}
    BASE_LINK = os.environ.get('SKYNET_EMAIL_LINK')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # MAIL_SERVER = 'mail.server.here'
    # MAIL_PORT = 587
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or DEF_SQL_DEBUG


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or DEF_SQL_TEST


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEF_SQL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
