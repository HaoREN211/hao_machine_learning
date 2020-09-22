# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/22 17:44
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main.routes import index
