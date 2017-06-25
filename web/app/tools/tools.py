# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
import time
from sqlalchemy.exc import SQLAlchemyError

from ..models import User, timedelta, datetime
from flask import current_app
from app import db
from ..tools.rpc_client import TimeoutServerProxy
# http://127.0.0.1:8001
rpc_cli = TimeoutServerProxy('http://127.0.0.1:8003', allow_none=True, timeout=180)


def new_user_count(time_interval, page):
    """
    查看一段时间内新增用户
    :return:
    """
    today = datetime.today()
    new_users = User.query.filter(today - timedelta(time_interval) < User.member_since).\
        paginate(page, current_app.config['SKYNET_USERS_PER_PAGE'], error_out=False)

    return new_users


def login_user_count(time_interval, page):
    """
    查看一段时间内登录用户
    :return:
    """
    today = datetime.utcnow()
    new_users = User.query.filter(today - timedelta(hours=time_interval) < User.last_seen).\
        paginate(page, current_app.config['SKYNET_USERS_PER_PAGE'], error_out=False)
    return new_users

