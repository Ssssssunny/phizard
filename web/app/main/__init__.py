# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, forms, users, emoji

