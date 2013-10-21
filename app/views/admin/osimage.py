# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.ext.wtf import Form, SelectField, TextField, BooleanField, Required

import simplejson as json

from app.models import *
from app.apc import APC
from app.dicts import *
from app.views import *

mod = Blueprint('osimage', __name__, url_prefix='/admin/osimage')


@mod.route('/')
def index():
    form = OSImageForm()
    form.cluster_id.choices = [(c.id, c.name) for c in Cluster.query.all()]
    osimage = OS_Image.query.all()
    cluster = Cluster.query.all()
    cluster_dict = cluster2dict()

    return render_template('admin/osimage/index.html', cluster=cluster, cluster_dict=cluster_dict, osimage=osimage, form=form)


@mod.route('/add', methods=['POST'])
def add():
    form = OSImageForm()
    form.cluster_id.choices = [(c.id, c.name) for c in Cluster.query.all()]

    if not form.validate_on_submit():
        flash(u'镜像选择有误！', 'error')
        return redirect(url_for('.index'))

    if OS_Image.query.filter(and_(OS_Image.cluster_id==form.cluster_id.data, OS_Image.sunstone_id==form.sunstone_id.data)).count() > 0:
        flash(u"该镜像已经添加！", 'error')
        return redirect(url_for('.index'))

    if form.name.data == '':
        form.name.data = form.sunstone_name.data

    osimage = OS_Image(form.cluster_id.data, form.sunstone_id.data,
                form.sunstone_name.data, form.name.data, 0)
    db.session.add(osimage)
    db.session.commit()

    return redirect(url_for('.index'))


@mod.route('/<osimage_id>/edit',  methods=['GET', 'POST'])
@check_load_osimage
def edit(osimage, **kvargs):
    ret = {}

    if request.form['name'] == '':
        os_name = osimage.sunstone_name
    else:
        os_name = request.form['name']

    ret['os_name'] = os_name
    osimage.name = os_name

    try:
        db.session.add(osimage)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u'修改成功'
    except:
        ret['status'] = 0
        ret['msg'] = u'修改失败'

    return json.dumps(ret)


@mod.route('/<int:osimage_id>/delete', methods=['POST'])
@check_load_osimage
def delete(osimage, **kvargs):
    ret = {}

    try:
        db.session.delete(osimage)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


class OSImageForm(Form):
    cluster_id = SelectField(u'Cluster', coerce=int)
    sunstone_id = TextField(u'Sunstone ID', validators=[Required()])
    sunstone_name = TextField(u'Sunstone Name', validators=[Required()])
    name = TextField(u'Name', validators=[])
