# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2020/9/23 14:19
# IDE：PyCharm

from app import db
from flask import render_template, request
from app.scenes.fraud_phone import bp
from app.forms.data_description import DataFieldDescriptionForm
from app.forms.model import ModelSelectedForm
from app.models.data_description import DataFieldDescription
from app.forms import flash_form_errors
from app.tools.model import machine_learning_model

# 展示欺诈电话相关的数据信息，包括各字段的最大值、最小值、平均值
@bp.route('/data', methods=['GET', 'POST'])
def data():
    # scene_id=1表示是电话诈骗的场景
    form = DataFieldDescriptionForm(scene_id=1)
    list_value = []
    max_value, min_value, mean_value, data_cnt = None, None, None, None
    if request.method == "POST":
        if form.create_submit.data and form.is_submitted():
            if form.validate():
                target_field_name = DataFieldDescription.query.filter_by(id=int(form.field_name.data)).first()
                list_value = [x[0] for x in list(db.session.execute("SELECT "+target_field_name.field_name+" FROM data_fraud_phone"))]
                data_cnt = len(list_value)
                max_value = max(list_value)
                min_value = min(list_value)
                mean_value = round(sum(list_value)/len(list_value), 2)
                if len(list_value) > 10:
                    list_value = list_value[:10]
            else:
                flash_form_errors(form)
    return render_template("fraud_phone/data_description.html", form=form, list_value=list_value, data_cnt=data_cnt,
                           min_value=min_value, max_value=max_value, mean_value=mean_value)


# 模型选择
@bp.route('/model', methods=['GET', 'POST'])
def model():
    # 在选择入模的特征时，去掉标签列。
    target_field_name = [x for x in DataFieldDescription.query.all() if x.field_name != "label"]
    model_form = ModelSelectedForm(scene_id=1)

    # 如果提交了表单，则验证提交表单的内容。
    # 表单内容没有错误的话，则开始训练和测试模型
    model_result = None
    if request.method == "POST":
        if model_form.create_submit.data and model_form.is_submitted():
            if not model_form.validate():
                flash_form_errors(model_form)
            else:
                model_result = machine_learning_model(model_form.field_selected.data,
                                       int(model_form.model_name.data),
                                       int(model_form.scene_id.data))
    return render_template("fraud_phone/model.html", fields = target_field_name, model_form=model_form,
                           model_result=model_result)
