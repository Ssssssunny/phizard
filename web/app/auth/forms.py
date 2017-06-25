# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


# 登录表单
class RegisterForm(Form):
    username = StringField('Username', validators=[
            DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  'Usernames must have only letters, '
                                                  'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    tag = BooleanField('Are you admin')
    submit = SubmitField('Register')


# 登录表单
class LoginForm(Form):
    username = StringField('Username', validators=[
            DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  'Usernames must have only letters, '
                                                  'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
