# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 23:11
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models.user import User

class UserForm(FlaskForm):
    username = StringField("用户账号名", validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码:', validators=[DataRequired(), EqualTo('password')])
    SubmitField = SubmitField("注册")

    def validate_username(self, username):
        users = User.query.filter_by(username=str(username.data)).all()
        if len(users)>0:
            raise ValidationError('当前用户名已被占用，请使用另外一个用户名。')

class LoginForm(FlaskForm):
    username = StringField("用户账号名：", validators=[DataRequired()])
    password = PasswordField("密码：", validators=[DataRequired()])
    remember_me = BooleanField("请记住我")
    submit = SubmitField("登录")