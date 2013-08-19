# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

mod = Blueprint('buy', __name__, url_prefix='/buy')


@mod.route('/')
def index():
    return render_template('buy/index.html')
