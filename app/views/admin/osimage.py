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
    form.idc_id.choices = [(i.id, i.name) for i in IDC.query.all()]
    osimage = OS_Image.query.all()
    idc = IDC.query.all()
    idc_dict = idc2dict()

    return render_template('admin/osimage/index.html', idc=idc, idc_dict=idc_dict, osimage=osimage, form=form)


@mod.route('/add', methods=['POST'])
def add():
    form = OSImageForm()
    form.idc_id.choices = [(i.id, i.name) for i in IDC.query.all()]

    if not form.validate_on_submit():
        flash(u'镜像选择有误！', 'error')
        return redirect(url_for('.index'))

    if OS_Image.query.filter(and_(OS_Image.idc_id==form.idc_id.data, OS_Image.sunstone_id==form.sunstone_id.data)).count() > 0:
        flash(u"该镜像已经添加！", 'error')
        return redirect(url_for('.index'))

    if form.name.data == '':
        form.name.data = form.sunstone_name.data

    osimage = OS_Image(form.idc_id.data, form.sunstone_id.data,
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
    except:
        ret['status'] = 0

    return json.dumps(ret)


@mod.route('/<osimage_id>/delete')
@check_load_osimage
def delete(osimage, **kvargs):
    db.session.delete(osimage)
    db.session.commit()
    return redirect(url_for('.index'))


class OSImageForm(Form):
    idc_id = SelectField(u'IDC', coerce=int)
    sunstone_id = TextField(u'Sunstone ID', validators=[Required()])
    sunstone_name = TextField(u'Sunstone Name', validators=[Required()])
    name = TextField(u'Name', validators=[])
