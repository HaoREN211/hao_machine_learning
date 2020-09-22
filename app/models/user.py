# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 23:10
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


class User(UserMixin, db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='用户主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户账号名')
    password_hash = db.Column(db.String(128), comment='用户密码')
    is_admin = db.Column(db.Boolean, comment='是否是超级管理员', default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))