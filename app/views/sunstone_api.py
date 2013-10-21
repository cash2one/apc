# -*- coding: utf-8 -*-

from flask import Blueprint, request

import simplejson as json

from app.apc import APC
from app.views import *
from app.models import *

mod = Blueprint('sunstone', __name__, url_prefix='/sunstone')


@mod.route('/cluster/<int:cluster_id>/vnet')
@check_load_cluster
def vnet(cluster, **kvargs):
    apc = APC(cluster)
    vnet = apc.vnet_sunstone()
    return json.dumps(vnet)


@mod.route('/cluster/<int:cluster_id>/image')
@check_load_cluster
def image(cluster, **kvargs):
    apc = APC(cluster)
    image = apc.image_sunstone()
    return json.dumps(image)


@mod.route('/cluster/<int:cluster_id>/datastore')
@check_load_cluster
def datastore(cluster, **kvargs):
    apc = APC(cluster)
    datastore = apc.datastore_sunstone()
    return json.dumps(datastore)


@mod.route('/datastore', methods=['POST'])
def datastore_live():
    cluster = Cluster('', '', '', '', request.form['sunstone_api'], request.form['api_auth'], '', '')
    apc = APC(cluster)
    datastore = apc.datastore_sunstone()
    return json.dumps(datastore)
