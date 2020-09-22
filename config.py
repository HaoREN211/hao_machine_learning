# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2019/12/21 8:04
# IDE：PyCharm

import os
from config_db import ConfigDb


class Config(object):
    # 分页功能，每页显示的个数
    POSTS_PER_PAGE = 10

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-hao-guess'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = ConfigDb.USERNAME
    PASSWORD = ConfigDb.PASSWORD
    HOST = ConfigDb.HOST
    PORT = ConfigDb.PORT
    DATABASE = ConfigDb.DATABASE
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5

    BOOTSTRAP_SERVE_LOCAL = True
