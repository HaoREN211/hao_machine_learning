# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/23 14:19
# IDE：PyCharm

from app import db
from flask import render_template, request
from app.scenes.fraud_phone import bp
from app.forms.data_description import DataFieldDescriptionForm
from app.models.data_description import DataFieldDescription
from app.forms import flash_form_errors

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
    return render_template("data_description.html", form=form, list_value=list_value, data_cnt=data_cnt,
                           min_value=min_value, max_value=max_value, mean_value=mean_value)
