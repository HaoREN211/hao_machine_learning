# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/23 18:00
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT

class DataFieldDescription(db.Model):
    __table_args__ = {'comment': '各机器学习所用数据表的字段列表'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='域主键')
    field_name = db.Column(db.String(100), comment='字段名')
    field_description = db.Column(db.String(100), comment='字段解释')
    scene_id = db.Column(db.Integer, comment='机器学习主题')
