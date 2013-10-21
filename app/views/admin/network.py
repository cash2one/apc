# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.ext.wtf import Form, SelectField, TextField, BooleanField, Required
from sqlalchemy import and_

import simplejson as json

from app import db
from app.models import *
from app.apc import APC
from app.views import *
from app.dicts import *

mod = Blueprint('network', __name__, url_prefix='/admin/network')


@mod.route('/')
def index():
    form = NetworkForm()
    form.cluster_id.choices = [(i.id, i.name) for i in Cluster.query.all()]
    cluster = Cluster.query.all()
    cluster_dict = cluster2dict()
    vnet = Network.query.all()

    return render_template('admin/network/index.html', form=form, cluster=cluster, cluster_dict=cluster_dict, vnet=vnet)


@mod.route('/add', methods=['POST'])
def add():
    form = NetworkForm()
    form.cluster_id.choices = [(i.id, i.name) for i in IDC.query.all()]

    if not form.validate_on_submit():
        flash(u'网段选择有误！', 'error')
        return redirect(url_for('.index'))

    if Network.query.filter(and_(Network.cluster_id==form.cluster_id.data, Network.sunstone_id==form.sunstone_id.data)).count() > 0:
        flash(u"该网段已经添加！", 'error')
        return redirect(url_for('.index'))

    if form.name.data == '':
        form.name.data = form.sunstone_name.data

    network = Network(form.cluster_id.data, form.sunstone_id.data, 
                      form.sunstone_name.data, form.name.data, 0)
    db.session.add(network)
    db.session.commit()

    return redirect(url_for('.index'))


@mod.route('/<int:network_id>/edit',  methods=['GET', 'POST'])
@check_load_network
def edit(network, **kvargs):
    ret = {}

    if request.form['name'] == '':
        net_name = network.sunstone_name
    else:
        net_name = request.form['name']

    ret['net_name'] = net_name
    network.name = net_name

    try:
        db.session.add(network)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u'修改成功'
    except:
        ret['status'] = 0
        ret['msg'] = u'修改失败'

    return json.dumps(ret)


@mod.route('/<int:network_id>/delete', methods=['POST'])
@check_load_network
def delete(network, **kvargs):
    ret = {}

    try:
        db.session.delete(network)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


class NetworkForm(Form):
    cluster_id = SelectField(u'Cluster', coerce=int)
    sunstone_id = TextField(u'Sunstone ID', validators=[Required()])
    sunstone_name = TextField(u'Sunstone Name', validators=[Required()])
    name = TextField(u'Name', validators=[])
