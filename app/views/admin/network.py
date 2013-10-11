# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.wtf import Form, SelectField, TextField, BooleanField

import simplejson as json

from app import db
from app.models import *
from app.apc import APC
from app.views import *
from app.dicts import *

mod = Blueprint('network', __name__, url_prefix='/admin/network')


@mod.route('/')
def index():
    idc = IDC.query.all()
    idc_dict = idc2dict()
    vnet = Network.query.all()
    apc = APC()
    vnet_sunstone = apc.vnet_sunstone()

    return render_template('admin/network/index.html', idc=idc, 
                            idc_dict=idc_dict, vnet=vnet, vnet_sunstone=vnet_sunstone)


@mod.route('/add', methods=['POST'])
def add():
    form = NetworkForm()

    if form.name.data == '':
        form.name.data = form.sunstone_name.data

    network = Network(form.idc_id.data, form.sunstone_id.data, 
                      form.sunstone_name.data, form.name.data, 0)
    db.session.add(network)
    db.session.commit()

    return redirect(url_for('.index'))


@mod.route('/<network_id>/edit',  methods=['GET', 'POST'])
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
    except:
        ret['status'] = 0

    return json.dumps(ret)


@mod.route('/<network_id>/delete')
@check_load_network
def delete(network, **kvargs):
    db.session.delete(network)
    db.session.commit()
    return redirect(url_for('.index'))


class NetworkForm(Form):
    idc_id = SelectField(u'IDC', coerce=int)
    sunstone_id = SelectField(u'Sunstone ID', coerce=int)
    sunstone_name = TextField(u'Sunstone Name', validators=[])
    name = TextField(u'Name', validators=[])
