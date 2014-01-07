# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify, flash

import simplejson as json

from app import app, db
from app.views import *
from app.utils import *
from app.dicts import *
from app.models import *
from app.vm import VMC
from app.sunstone import Sunstone

mod = Blueprint('vm', __name__, url_prefix='/vm')


@mod.route('/test', defaults={'page':1})
@mod.route('/test/page/<int:page>')
def test(page, **kvargs):
    vms = VM.query.filter(VM.if_test==1).order_by(VM.hostname.asc()).paginate(page, per_page=15, error_out=True)
    return render_template('vm/test.html', vms=vms)


@mod.route('/production', defaults={'page':1})
@mod.route('/production/page/<int:page>')
def production(page, **kvargs):
    vms = VM.query.filter(VM.if_test!=1).order_by(VM.hostname.asc()).paginate(page, per_page=15, error_out=True)
    return render_template('vm/production.html', vms=vms)


@mod.route('/<int:vm_id>/view')
@check_load_vm
def view(vm, **kvargs):
    vminst = VMC()
    vm_detail = vminst.detail(vm)
    network_dict = network2dict()
    cpu = [x.cpu for x in db.session.query(CPU_Mem.cpu.distinct().label('cpu')).order_by(CPU_Mem.cpu).all()]
    mem = CPU_Mem.query.filter(CPU_Mem.cpu==vm.cpu).order_by(CPU_Mem.mem).all()
    return render_template('vm/view.html', vm=vm, cpu=cpu, mem=mem, vm_detail=vm_detail, network_dict=network_dict)


@mod.route('/<int:vm_id>/delete', methods=['POST'])
@check_load_vm
def delete(vm, **kvargs):
    vminst = VMC()
    status = 1 if vminst.delete(vm) else 0
    return jsonify(status=status)


@mod.route('/action', methods=['POST'])
def action_mult():
    status = 1
    vminst = VMC()

    try:
        action = request.form['action']
    except:
        action = None

    if request.form['vmlist'] == "":
        vmlist = []
    else:
        vmlist = request.form['vmlist'].split(',')

    for x in vmlist:
        vm = VM.query.get(int(x))
        if action == 'delete':
            if not vminst.delete(vm):
                status = 0
        if action == 'start':
            if not vminst.start(vm):
                status = 0
        if action == 'poweroff':
            if not vminst.poweroff(vm):
                status = 0
        if action == 'poweroff_hard':
            if not vminst.poweroff_hard(vm):
                status = 0
        if action == 'reboot':
            if not vminst.reboot(vm):
                status = 0
        if action == 'reboot_hard':
            if not vminst.reboot_hard(vm):
                status = 0
        if action == 'recreate':
            if not vminst.recreate(vm):
                status = 0

    vminst.refresh()

    if status:
        flash(u'操作成功', 'success')
    else:
        flash(u'操作失败', 'error')
    return redirect(request.referrer)


@mod.route('/<int:vm_id>/rename', methods=['GET', 'POST'])
@check_load_vm
def rename(vm, **kvargs):
    try:
        newname = request.form['data'] or vm.hostname
        vminst = VMC()
        vminst.rename(vm, newname)
        vm.hostname = newname
        db.session.add(vm)
        db.session.commit()
        status = 1
    except:
        status = 0

    return jsonify(status=status)


@mod.route('/<int:vm_id>/resize', methods=['GET', 'POST'])
@check_load_vm
def resize(vm, **kvargs):
    try:
        vminst = VMC()
        cpu = request.form['cpu'] or vm.cpu
        mem = request.form['mem'] or vm.mem
        vminst.resize(vm, cpu, mem)
        status = 1
    except:
        status = 0

    return jsonify(status=status)


@mod.route('/<int:vm_id>/attach_nic', methods=['GET', 'POST'])
@check_load_vm
def attach_nic(vm, **kvargs):
    #try:
    vminst = VMC()
    network_id = request.form['network_id']
    vminst.attach_nic(vm, network_id)
    flag = True
    sunstone = Sunstone(vm.cluster)
    while flag:
        resp = sunstone.vm_id(vm.vm_id)
        info = json.loads(resp.data)['VM']
        if int(info['STATE']) == 3:
            flag = False
    status = 1
    #except:
    #    status = 0

    return jsonify(status=status)


@mod.route('/<int:vm_id>/detach_nic', methods=['GET', 'POST'])
@check_load_vm
def detach_nic(vm, **kvargs):
    try:
        vminst = VMC()
        nic_id = request.form['nic_id']
        vminst.detach_nic(vm, nic_id)
        flag = True
        sunstone = Sunstone(vm.cluster)
        while flag:
            resp = sunstone.vm_id(vm.vm_id)
            info = json.loads(resp.data)['VM']
            if int(info['STATE']) == 3:
                flag = False
        status = 1
    except:
        status = 0

    return jsonify(status=status)


@mod.route('/<int:vm_id>/redesc', methods=['GET', 'POST'])
@check_load_vm
def redesc(vm, **kvargs):
    try:
        desc = request.form['data'] or vm.desc
        vm.desc = desc
        db.session.add(vm)
        db.session.commit()
        status = 1
    except:
        status = 0

    return jsonify(status=status)


@mod.route('/refresh')
def refresh():
    vminst = VMC()
    if vminst.refresh():
        flash(u'刷新成功', 'success')
    else:
        flash(u'刷新失败', 'error')
    return redirect(request.referrer)
