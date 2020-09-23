# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/23 16:32
# IDE：PyCharm

from app.forms import RenderForm
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.models.data_description import DataFieldDescription

class DataFieldDescriptionForm(RenderForm):
    field_name = SelectField("字段名", validators=[DataRequired()],
                             coerce=int, choices=[(0, " ")], default=0,
                             render_kw={"class": "select-control"})
    scene_id = HiddenField("机器学习主题")

    create_submit = SubmitField("确认", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(DataFieldDescriptionForm, self).__init__(*args, **kwargs)
        self.scene_id.data = kwargs["scene_id"]
        if kwargs["scene_id"] == 1:
            self.field_name.choices.extend([(int(x.id), x.field_description) for x in DataFieldDescription.query.all()])
