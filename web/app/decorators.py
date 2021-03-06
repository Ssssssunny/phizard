# # -*- coding: utf-8 -*-
#
# """
# decorators
#
# created: 2017-03-01
#
# by: Yr
# """
# import traceback
#
# from flask import g, request
# from flask_httpauth import HTTPBasicAuth
#
# from app.models import User, AnonymousUser
#
# auth = HTTPBasicAuth()
#
#
# @auth.verify_password
# def verify_password(email_or_token, password):
#     if email_or_token == '':
#         g.current_user = AnonymousUser()
#         return True
#     if password == '':
#         g.current_user = User.verify_auth_token(email_or_token)
#         g.token_used = True
#         return g.current_user is not None
#     user = User.query.filter_by(email=email_or_token).first()
#     if not user:
#         return False
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)