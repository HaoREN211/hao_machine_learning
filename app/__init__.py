# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/22 17:18
# IDE：PyCharm

# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2019/12/21 7:55
# IDE：PyCharm

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_moment import Moment
from logging.handlers import RotatingFileHandler
import logging
import os


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

# 要求用户登录
login.login_view = 'auth.login'
login.login_message = '请先进行登录.'
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)
    moment.init_app(app)
    babel.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.scenes.fraud_phone import bp as fraud_phone_bp
    app.register_blueprint(fraud_phone_bp, url_prefix="/fraud_phone")

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        # 日志文件的大小限制为1000KB，并只保留最后的十个日志文件作为备份。
        file_handler = RotatingFileHandler('logs/enterprise.log', maxBytes=1024000,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('enterprise startup')

    return app
