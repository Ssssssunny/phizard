# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
from flask import render_template, request, current_app, redirect, make_response, url_for, flash
from flask_login import current_user, login_required
from . import main
from app import db
from ..models import User
from .forms import UserForm


@main.route('/users')
@login_required
def users():
    userform = UserForm()

    page = request.args.get('page', 1, type=int)

    pagination = User.query.filter_by(tag=1).order_by(User.member_since.desc()).\
        paginate(page, current_app.config['SKYNET_USERS_PER_PAGE'], error_out=False)

    all_users_detail = pagination.items

    return render_template('users.html', users=all_users_detail, pagination=pagination, endpoint='.users',
                           form=userform)
