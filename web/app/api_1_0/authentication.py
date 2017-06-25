from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from .errors import unauthorized, forbidden
from ..models import AnonymousUser, User
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    print '-------------------email_or_token:',email_or_token
    print '-------------------password:', password
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    tag = user.verify_password(password)
    return tag


@auth.error_handler
def auth_error():
    print '-------------auth_error'
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    print '-------------before_request'
    if g.current_user.is_anonymous:
        return forbidden('Unconfirmed account')


@api.route('/token')
def get_token():
    print '-------------get_token'
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
