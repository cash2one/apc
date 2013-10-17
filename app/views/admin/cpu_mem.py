# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask.ext.wtf import Form, BooleanField, TextField, validators, Required, Regexp

import simplejson as json

from app import db
from app.models import *
from app.views import *
from app.utils import *

mod = Blueprint('cpu_mem', __name__, url_prefix='/admin/cpu_mem')


@mod.route('/', methods=['GET'])
def index():
    form = CPUMemForm()
    cpu_mem = CPU_Mem.query.order_by(CPU_Mem.cpu.asc(),CPU_Mem.mem.asc()).all()
    return render_template('admin/cpu_mem/index.html', cpu_mem=cpu_mem, form=form)


@mod.route('/add', methods=['POST'])
def add():
    form = CPUMemForm()

    if not form.validate_on_submit():
        for k in form.errors.keys():
            flash(' '.join(form.errors[k]), 'error')
        return redirect(url_for('.index'))

    if CPU_Mem.query.filter(and_(CPU_Mem.cpu==form.cpu.data, CPU_Mem.mem==form.mem.data)).count() > 0:
        flash(u"该方案已经添加", 'error')
        return redirect(url_for('.index'))
   
    cpu_mem = CPU_Mem(form.cpu.data, form.mem.data) 
    db.session.add(cpu_mem)
    db.session.commit()
    flash(u"添加成功", 'success')

    return redirect(url_for('.index'))


@mod.route('/<int:cpumem_id>/edit', methods=['POST'])
@check_load_cpumem
def edit(cpumem, **kvargs):
    ret = {}
    form = CPUMemForm(obj=cpumem, csrf_enabled=False)

    if not form.validate_on_submit():
        ret['status'] = 0
        ret['msg'] = []
        for f in form.errors.keys():
            ret['msg'].append(' '.join((form.errors[f])))
        return json.dumps(ret)

    try:
        form.populate_obj(cpumem)
        db.session.add(cpumem)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = [u"编辑成功"]
    except:
        ret['status'] = 0
        ret['msg'] = [u"保存失败"]

    return json.dumps(ret)


@mod.route('/<int:cpumem_id>/delete')
@check_load_cpumem
def delete(cpumem, **kvargs):
    try:
        db.session.delete(cpumem)
        db.session.commit()
        flash(u"删除成功", 'success')
    except:
        flash(u"删除失败", 'error')

    return redirect(url_for('.index'))


class CPUMemForm(Form):
    cpu = TextField(u'CPU', validators=[Regexp('^[0-9]+$', message=u'CPU核数必须为数字')])
    mem = TextField(u'MEM', validators=[Regexp('^[0-9]+$', message=u'内存大小必须为数字')])
