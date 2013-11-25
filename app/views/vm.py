# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify, flash

import simplejson as json

from app import app, db
from app.views import *
from app.utils import *
from app.vm import VMC

mod = Blueprint('vm', __name__, url_prefix='/vm')


@mod.route('/<int:vm_id>/delete', methods=['POST'])
@check_load_vm
def delete(vm, **kvargs):
    vminst = VMC()
    status = 1 if vminst.delete(vm) else 0
    return jsonify(status=status)


@mod.route('/delete', methods=['POST'])
def delete_mult():
    status = 1
    vminst = VMC()
    try:
        ret_format = request.form['format']
    except:
        ret_format = "html"

    if request.form['vmlist'] == "":
        vmlist = []
    else:
        vmlist = request.form['vmlist'].split(',')
    for x in vmlist:
        vm = VM.query.get(int(x))
        print vm
        if not vminst.delete(vm):
            status = 0

    if ret_format == "html":
        return redirect(request.referrer)
    else:
        return jsonify(status=status)


@mod.route('/<int:vm_id>/rename', methods=['GET', 'POST'])
@check_load_vm
def rename(vm, **kvargs):
    try:
        newname = request.form['hostname'] or vm.hostname
        vminst = VMC()
        vminst.rename(vm, newname)
        vm.hostname = newname
        db.session.add(vm)
        db.session.commit()
        status = 1
    except:
        status = 0

    return jsonify(status=status)


@mod.route('/refresh')
def refresh():
    vminst = VMC()
    if vminst.refresh:
        flash(u'刷新成功', 'success')
    else:
        flash(u'刷新失败', 'success')
    return redirect(request.referrer)
