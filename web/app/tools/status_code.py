# -*- coding: utf-8 -*-

"""
status code

created: 2017-02-20

by: Yr
"""

from flask import jsonify


class SystemErrorCode():
    """ 系统服务状态码 """
    @staticmethod
    def operate_succeed(data={}, message='operate successful'):
        """操作成功"""
        response = jsonify({'status_code': 200, 'data': data, 'message': message})
        return response

    @staticmethod
    def operate_failed(message='operate failed'):
        """一般性异常 """
        response = jsonify({'status_code': 201, 'data': {}, 'message': message})
        return response
