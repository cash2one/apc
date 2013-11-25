# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.wtf import Form, SelectField, TextField, BooleanField, Required, Length
from flask.ext.login import current_user
from flask.ext.paginate import Pagination

from sqlalchemy import distinct

import simplejson as json

from app import app
from app.models import *
from app.dicts import *
from app.views import *
from app.occi import OCCI
from app.order import *
from app.vm import VMC

mod = Blueprint('order', __name__, url_prefix='/order')


@mod.route('/new', methods=['GET', 'POST'])
def new():
    form = OrderForm()
    form.cluster_id.choices = [(i.id, i.name) for i in Cluster.query.all()]
    form.cnt.choices = [(i, i) for i in range(1, 11)]
    cpu = db.session.query(CPU_Mem.cpu.distinct().label('cpu')).order_by(CPU_Mem.cpu).all()

    if not form.validate_on_submit():
        edit = 1 if request.method=='POST' else 0
        return render_template('order/new.html', form=form, cpu=cpu, edit=edit, price=app.config['PRICE'])

    orders = Orders(form.cluster_id.data, form.cpu.data, form.mem.data, form.network.data, form.disk.data, 
                    request.form['os_id'], form.cnt.data, 0, current_user.user_id, form.desc.data, form.days.data)
    db.session.add(orders)
    db.session.commit()

    return redirect(url_for('my_order.list'))


@mod.route('/list', defaults={'page':1})
@mod.route('/list/page/<int:page>')
def list(page, **kvargs):
    order = Orders.query.order_by(Orders.id.desc()).paginate(page, per_page=15, error_out=True)
    return render_template('order/list.html', order=order, order_status=app.config['ORDER_STATUS'])


@mod.route('/<int:order_id>/view')
@check_load_order
def view(order, **kvargs):
    network_dict = network2dict()
    form = OrderForm(obj=order)
    return render_template('order/view.html', order=order, network_dict=network_dict, form=form, config=app.config)


@mod.route('/<int:order_id>/edit', methods=['GET', 'POST'])
@check_load_order
def edit(order, **kvargs):
    order.disk = ','.join(str(x) for x in order.disk)
    order.network = ','.join(str(x) for x in order.network)
    cpu = db.session.query(CPU_Mem.cpu.distinct().label('cpu')).order_by(CPU_Mem.cpu).all()
    form = OrderForm(obj=order)
    form.cluster_id.choices = [(i.id, i.name) for i in Cluster.query.all()]
    form.cnt.choices = [(i, i) for i in range(1, 11)]

    if not form.validate_on_submit():
        return render_template('order/edit.html', form=form, cpu=cpu, order=order, edit=1, price=app.config['PRICE'])

    form.populate_obj(order)
    db.session.add(order)
    db.session.commit()

    return redirect(url_for('my_order.view', order_id=order.id))


@mod.route('/<int:order_id>/delete', methods=['GET', 'POST'])
@check_load_order
def delete(order, **kvargs):
    ret = {}
    vmc = VMC()

    try:
        for x in order.vm:
            vmc.delete(x)
        db.session.delete(order)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


@mod.route('/<int:order_id>/approve')
@check_load_order
def approve(order, **kvargs):
    orderc = OrderC(order)
    if orderc.create_vm():
        flash(u'虚拟机创建成功', 'success')
    else:
        flash(u'虚拟机创建失败', 'error')
    return redirect(url_for('.view', order_id=order.id))


@mod.route('/<int:order_id>/cancle')
@check_load_order
def cancle(order, **kvargs):
    orderc = OrderC(order)
    orderc.cancle()
    flash(u'取消申请', '')
    return redirect(request.referrer)


@mod.route('/<int:order_id>/reject')
@check_load_order
def reject(order, **kvargs):
    orderc = OrderC(order)
    orderc.reject()
    return redirect(url_for('.view', order_id=order.id))


@mod.route('/<int:order_id>/refresh')
@check_load_order
def refresh(order, **kvargs):
    vminst = VMC()
    if vminst.refresh():
        flash(u'刷新成功', 'success')
    else:
        flash(u'刷新失败', 'success')
    return redirect(request.referrer)


@mod.route('/<int:order_id>/state_change')
@check_load_order
def state_change(order, **kvargs):
    new_state = request.args.get('state', order.status)
    order.status = new_state
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('.view', order_id=order.id))


class OrderForm(Form):
    desc = TextField(u'用途', validators=[Required(message=u"不能为空")])
    cluster_id = SelectField(u'集群', coerce=int)
    cpu = TextField(u'CPU', validators=[Required()])
    mem = TextField(u'内存', validators=[Required()])
    network = TextField(u'网络', validators=[])
    disk = TextField(u'磁盘', validators=[])
    os_id = TextField(u'操作系统', validators=[Required()])
    cnt = SelectField(u'台数', coerce=int)
    days = TextField(u'天数', validators=[Length(max=30)])
