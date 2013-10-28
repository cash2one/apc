# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.wtf import Form, SelectField, TextField, BooleanField, Required
from flask.ext.login import current_user
from flask.ext.paginate import Pagination

from sqlalchemy import distinct

import simplejson as json

from app import app
from app.models import *
from app.dicts import *
from app.views import *

mod = Blueprint('order', __name__, url_prefix='/order')


@mod.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    form.cluster_id.choices = [(i.id, i.name) for i in Cluster.query.all()]
    form.cnt.choices = [(i, i) for i in range(1, 11)]
    cpu = db.session.query(CPU_Mem.cpu.distinct().label('cpu')).order_by(CPU_Mem.cpu).all()
    return render_template('order/index.html', form=form, cpu=cpu)


@mod.route('/new', methods=['POST'])
def new():
    form = OrderForm()
    orders = Orders(form.cluster_id.data, form.cpu.data, form.mem.data, form.network.data, form.disk.data, 
                request.form['os-id'], form.cnt.data, 0, current_user.user_id, form.desc.data)
    db.session.add(orders)
    db.session.commit()
    return redirect(url_for('.index'))


@mod.route('/list', defaults={'page':1})
@mod.route('/list/page/<int:page>')
def list(page, **kvargs):
    order = Orders.query.paginate(page, per_page=15, error_out=True)
    return render_template('order/list.html', order=order, order_status=app.config['ORDER_STATUS'])


@mod.route('/<int:order_id>/delete', methods=['POST'])
@check_load_order
def delete(order, **kvargs):
    ret = {}

    try:
        db.session.delete(order)
        db.session.commit()
        ret['status'] = 1
        ret['msg'] = u"删除成功"
    except:
        ret['status'] = 0
        ret['msg'] = u"删除失败"

    return json.dumps(ret)


class OrderForm(Form):
    cluster_id = SelectField(u'集群', coerce=int)
    cpu = TextField(u'CPU', validators=[Required()])
    mem = TextField(u'内存', validators=[Required()])
    network = TextField(u'网络', validators=[Required()])
    disk = TextField(u'磁盘', validators=[Required()])
    osimage = TextField(u'操作系统', validators=[Required()])
    cnt = SelectField(u'台数', coerce=int)
    desc = TextField(u'简述', validators=[Required()])
