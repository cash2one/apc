# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

mod = Blueprint('idc', __name__, url_prefix='/admin/idc')


@mod.route('/')
def index():
    return render_template('admin/idc/index.html')
