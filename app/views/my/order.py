# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect
from flask.ext.login import current_user

from app import app
from app.models import *
from app.views import *
from app.dicts import *
from app.views.order import OrderForm
from app.vm import VMC

mod = Blueprint('my_order', __name__, url_prefix='/my/order')


@mod.route('/list', defaults={'page':1})
@mod.route('/list/page/<int:page>')
def list(page, **kvargs):
    order = Orders.query.filter(Orders.user_id==current_user.user_id).order_by(Orders.id.desc()).paginate(page, per_page=13, error_out=True)
    return render_template('my/order/list.html', order=order, order_status=app.config['ORDER_STATUS'])


@mod.route('/<int:order_id>/view')
@check_load_order
def view(order, **kvargs):
    network_dict = network2dict()
    form = OrderForm(obj=order)
    return render_template('my/order/view.html', order=order, network_dict=network_dict, form=form, config=app.config)
