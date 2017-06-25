# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

