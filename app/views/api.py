# -*- coding: utf-8 -*-

from flask import Blueprint, request

import simplejson as json

from app.models import *
from app.views import *

mod = Blueprint('api', __name__, url_prefix='/api')


@mod.route('/cluster/<int:cluster_id>')
@check_load_cluster
def cluster(cluster, **kvargs):
    return '{"cluster_id":%s , "cluster_name":"%s", "if_test":%s}' % \
            (cluster.id, cluster.name, cluster.if_test)


@mod.route('/cpu_scheme')
def cpu_scheme():
    ret = []

    for c in db.session.query(CPU_Mem.cpu.distinct().label('cpu')).order_by(CPU_Mem.cpu).all():
        ret.append(c.cpu)

    return json.dumps(ret)


@mod.route('/mem_scheme')
def mem_scheme():
    ret = []
    cpu = request.args.get('cpu')

    for m in CPU_Mem.query.filter_by(cpu=cpu).order_by(CPU_Mem.mem):
        ret.append(m.mem)

    return json.dumps(ret)


@mod.route('/network')
def network():
    ret = []
    cluster_id = request.args.get('cluster_id')

    for n in Network.query.filter_by(cluster_id=cluster_id).all():
        ret.append({'id':n.id, 'name':n.name, 'if_default':n.if_default})

    return json.dumps(ret)


@mod.route('/osimage')
def osimage():
    ret = []
    cluster_id = request.args.get('cluster_id')

    for i in OS_Image.query.filter_by(cluster_id=cluster_id).all():
        ret.append({'id':i.id, 'name':i.name})

    return json.dumps(ret)
