# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/9/23 16:31
# IDE：PyCharm

from flask_wtf import FlaskForm
from flask import flash

def flash_form_errors(form):
    for current_error_key in list(form.errors.keys()):
        for current_error in form.errors[current_error_key]:
            flash(current_error)

class RenderForm(FlaskForm):
    class Meta(FlaskForm.Meta):
        """
        https://www.jianshu.com/p/804cd09b8051
        重写render_field，实现Flask-Bootstrap与render_kw的class并存
        """
        def render_field(self, field, render_kw):
            other_kw = getattr(field, 'render_kw', None)
            if other_kw is not None:
                # 只保留自定义的class
                list_attribute_keep = ["class", "type", "onclick", "readonly", "data-dismiss", "step", "start"]

                for current_attribute in list_attribute_keep:
                    attribute_value = other_kw.get(current_attribute, None)
                    if attribute_value is not None:
                        render_kw[current_attribute] = attribute_value

                # quick_form 时外部传入的值
                class2 = render_kw.get('class', None)
            return field.widget(field, **render_kw)
