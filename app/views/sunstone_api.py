# -*- coding: utf-8 -*-

from flask import Blueprint

import simplejson as json

from app.apc import APC
from app.views import *

mod = Blueprint('sunstone', __name__, url_prefix='/sunstone')


@mod.route('/idc/<idc_id>/vnet')
@check_load_idc
def vnet(idc, **kvargs):
    apc = APC(idc)
    vnet = apc.vnet_sunstone()
    return json.dumps(vnet)


@mod.route('/idc/<idc_id>/image')
@check_load_idc
def image(idc, **kvargs):
    apc = APC(idc)
    image = apc.image_sunstone()
    return json.dumps(image)
