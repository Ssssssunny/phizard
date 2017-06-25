# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


# 登录表单
class UserForm(Form):
    userid = StringField('UserId', validators=[DataRequired()])
    role = SelectField('Roles', validators=[DataRequired()], choices=[('0', 'free (code: 1)'),
                                                                      ('1', 'Premium (code: 2)'),
                                                                      ('2', 'admin (code: 3)')])
    level = SelectField('Levels', validators=[DataRequired()], choices=[('0', 'low (code: 1)'),
                                                                        ('1', 'high (code: 9)')])
    submit = SubmitField('Submit')


