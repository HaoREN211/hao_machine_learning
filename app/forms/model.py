# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/10/20 10:44
# IDE：PyCharm

from app.forms import RenderForm
from wtforms import SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired

# 机器学习模型列表
class Model:
    list_models = [(1, "决策树")]



# 模型页面中，用于选择使用训练数据的模型
class ModelSelectedForm(RenderForm):
    model_name = SelectField("模型", validators=[DataRequired()],
                             coerce=int, choices=[], default=1,
                             render_kw={"class": "select-control"})
    field_selected = HiddenField("入模的特征",
                                 validators=[DataRequired(message="请选择入模的特征")])
    scene_id = HiddenField("场景ID",
                                 validators=[DataRequired(message="请输入场景ID")])
    create_submit = SubmitField("确认", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ModelSelectedForm, self).__init__(*args, **kwargs)
        list_model = Model()
        self.model_name.choices.extend(list_model.list_models)
        self.scene_id.data = kwargs["scene_id"]
