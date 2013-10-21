# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask.ext.wtf import Form, TextField, BooleanField, SelectField, Required, length

import simplejson as json

from app import db
from app.models import *
from app.views import *
from app.dicts import *

mod = Blueprint('cluster', __name__, url_prefix='/admin/cluster')


@mod.route('/')
def index():
    form = ClusterForm()
    cluster = Cluster.query.order_by(Cluster.name.asc()).all()
    idc_dict = idc2dict()
    return render_template('admin/cluster/index.html', form=form, cluster=cluster, idc_dict=idc_dict)


@mod.route('/add', methods=['GET', 'POST'])
def add():
    form = ClusterForm()
    form.idc_id.choices = [(i.id, i.name) for i in IDC.query.all()]

    if not form.validate_on_submit():
        return render_template('admin/cluster/add.html', form=form)

    try:
        cluster = Cluster(form.idc_id.data, form.name.data, form.host.data, form.occi_api.data, 
                    form.sunstone_api.data, form.api_auth.data, form.ds_id.data, form.ds_name.data)
        db.session.add(cluster)
        db.session.commit()
        flash(u'添加成功', 'success')
    except:
        flash(u'添加失败', 'error')

    return redirect(url_for('.index'))


@mod.route('/<int:cluster_id>/edit', methods=['GET', 'POST'])
@check_load_cluster
def edit(cluster, **kvargs):
    form = ClusterForm(obj=cluster)
    form.idc_id.choices = [(i.id, i.name) for i in IDC.query.all()]

    if not form.validate_on_submit():
        return render_template('admin/cluster/edit.html', form=form, cluster=cluster)

    try:
        form.populate_obj(cluster)
        db.session.add(cluster)
        db.session.commit()
        flash(u'修改成功', 'success')
    except:
        flash(u'保存失败', 'error')

    return redirect(url_for('.index'))


@mod.route('/<int:cluster_id>/delete', methods=['POST'])
@check_load_cluster
def delete(cluster, **kvargs):
    ret = {}

    try:
        db.session.delete(cluster)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


class ClusterForm(Form):
    idc_id = SelectField(u'机房', coerce=int)
    name = TextField(u'集群名称', validators=[Required()])
    host = TextField(u'中心节点', validators=[Required()])
    occi_api = TextField(u'OCCI API', validators=[Required()])
    sunstone_api = TextField(u'Sunstone API', validators=[Required()])
    api_auth = TextField(u'API Auth', validators=[Required()])
    ds_name = TextField(u'Datastore', validators=[])
    ds_id = TextField(u'Datastore ID', validators=[])
