# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

mod = Blueprint('cpu_mem', __name__, url_prefix='/admin/cpu_mem')


@mod.route('/')
def index():
    return render_template('admin/cpu_mem/index.html')
