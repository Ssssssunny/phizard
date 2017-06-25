# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
import hashlib
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, jsonify
from flask_login import login_required, logout_user, current_user, login_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.tag == 1:  # 普通员工不允许登录
            flash('You have no permission to login in.')
            return render_template('index.html')
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return render_template('index.html')

        flash('Password error')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册
    :return:
    """
    form = RegisterForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        tag = form.tag.data
        tag_value = 1  # 默认注册的是普通员工
        if tag:
            tag_value = 0

        user = User(username=username, password=password, tag=tag_value)
        try:
            db.session.add(user)
            db.session.commit()
            flash('register successful')
            return redirect(url_for('main.index'))
        except Exception:
            db.session.rollback()
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@auth.route('/get_token')
def get_token():

    username = request.args.get('username')
    pwd = request.args.get('password')
    print "=" * 30
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'code': 201, 'message': 'username is incorrect'})
    if not user.verify_password(pwd):
        return jsonify({'code': 201, 'message': 'password is incorrect'})

    token = user.generate_auth_token()
    return jsonify({'code': 200, 'data': {'token': token}})


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
