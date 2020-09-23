# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/23 14:18
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('fraud_phone', __name__)

from app.scenes.fraud_phone.routes import data