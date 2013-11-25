# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import and_

import time
import simplejson as json

from app.models import *
from app.sunstone import Sunstone

mod = Blueprint('hosts', __name__, url_prefix='/hosts')


@mod.route('/')
def index():
    hosts = Hosts.query.all() 
    return render_template('hosts/index.html', hosts=hosts)


@mod.route('/refresh')
def refresh():
    ts = int(time.time())
    for x in Cluster.query.all():
        sunstone = Sunstone(x)
        resp = sunstone.host()
        info = json.loads(resp.data)['HOST_POOL']['HOST']
        if type(info) == dict:
            info = [info]
        for y in info:
            hostinst = Hosts.query.filter(and_(Hosts.cluster_id==x.id, Hosts.sunstone_id==y['ID'])).first()
            if hostinst:
                hostinst.vmnum      = y['HOST_SHARE']['RUNNING_VMS']
                hostinst.max_cpu    = y['HOST_SHARE']['MAX_CPU']
                hostinst.cpu_usage  = y['HOST_SHARE']['CPU_USAGE']
                hostinst.used_cpu   = y['HOST_SHARE']['USED_CPU']
                hostinst.max_mem    = y['HOST_SHARE']['MAX_MEM']
                hostinst.mem_usage  = y['HOST_SHARE']['MEM_USAGE']
                hostinst.used_mem   = y['HOST_SHARE']['USED_MEM']
            else:
                hostinst = Hosts(x.id, y['ID'], y['NAME'], y['HOST_SHARE']['RUNNING_VMS'], 
                    y['HOST_SHARE']['MAX_CPU'], y['HOST_SHARE']['CPU_USAGE'], y['HOST_SHARE']['USED_CPU'], 
                    y['HOST_SHARE']['MAX_MEM'], y['HOST_SHARE']['MEM_USAGE'], y['HOST_SHARE']['USED_MEM'], ts)
            db.session.add(hostinst)
            db.session.commit()
    return redirect(url_for('.index'))
