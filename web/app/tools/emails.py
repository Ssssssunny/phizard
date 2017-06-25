# -*- coding: utf-8 -*-

"""
send email

created: 2017-06-06

by: Yr
"""
import requests
from flask import current_app, json


class EmailResquest:

    def send_email(self, to, subject, name, email, type=0, **kwargs):
        app = current_app._get_current_object()  # 获取邮件配置参数

        link = app.config['BASE_LINK']

        # 将模板中定义的变量 %name% 和 %url% 分别进行替换成真实值
        if type == 0:
            sub_vars = {
                        'to': [to],
                        'sub': {
                                '%email%': [email],
                                '%url%': [link],
                        }
            }
        else:
            sub_vars = {
                'to': [to],
                'sub': {
                    '%name%': [name]
                }
            }



        params = {
            "apiUser": app.config['API_USER'],
            "apiKey": app.config['API_KEY'],
            "templateInvokeName": app.config['INVORKTYPE'][type],
            "xsmtpapi": json.dumps(sub_vars),
            "from": 'service@sendcloud.im',
            "fromName": app.config['FROMNAME'],
            "subject": subject,
            "respEmailId": "true"
        }
        r = requests.post(app.config['MAIL_SERVER'], files={}, data=params)

        if u'"message":"请求成功"' not in r.text:
            print "Failed to send an email"
            return False
        return True
