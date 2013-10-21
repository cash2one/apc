# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask.ext.wtf import Form, TextField, BooleanField, Required, length

import simplejson as json

from app import db
from app.models import *
from app.views import *

mod = Blueprint('idc', __name__, url_prefix='/admin/idc')


@mod.route('/')
def index():
    form = IDCForm()
    idc = IDC.query.order_by(IDC.name.asc()).all()
    return render_template('admin/idc/index.html', form=form, idc=idc)


@mod.route('/add', methods=['GET', 'POST'])
def add():
    form = IDCForm()

    if not form.validate_on_submit():
        for k in form.errors.keys():
            flash(' '.join(form.errors[k]), 'error')
        return redirect(url_for('.index'))

    try:
        idc = IDC(form.name.data, form.chinese_name.data)
        db.session.add(idc)
        db.session.commit()
        flash(u"添加成功", 'success')
    except:
        flash(u"保存失败", 'error')

    return redirect(url_for('.index'))


@mod.route('/<int:idc_id>/edit', methods=['GET', 'POST'])
@check_load_idc
def edit(idc, **kvargs):
    ret = {}
    form = IDCForm(obj=idc, csrf_enabled=False)

    if not form.validate_on_submit():
        ret['status'] = 0
        ret['msg'] = []
        for f in form.errors.keys():
            ret['msg'].append(' '.join((form.errors[f])))
        return json.dumps(ret)

    try:
        form.populate_obj(idc)
        db.session.add(idc)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = [u"编辑成功"]
    except:
        ret['status'] = 0
        ret['msg'] = [u"保存失败"]

    return json.dumps(ret)


@mod.route('/<int:idc_id>/delete', methods=['GET', 'POST'])
@check_load_idc
def delete(idc, **kvargs):
    ret = {}

    try:
        db.session.delete(idc)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


class IDCForm(Form):
    name = TextField(u'名称', validators=[Required(message=u"名称不能为空"), length(max=20, message=u"名称最大长度20字节")])
    chinese_name = TextField(u'中文名称', validators=[length(max=20, message=u"中文名最大长度20字节")])
