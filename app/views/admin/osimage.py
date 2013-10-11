# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

import simplejson as json

from app.models import *
from app.apc import APC

mod = Blueprint('osimage', __name__, url_prefix='/admin/osimage')


@mod.route('/')
def index():
    apc = APC()
    image = apc.image_sunstone()

    return render_template('admin/osimage/index.html', image=image)
