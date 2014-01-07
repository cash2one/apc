# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect
from flask.ext.login import current_user

from sqlalchemy import and_

from app import app
from app.models import *
from app.vm import VMC

mod = Blueprint('my_vm', __name__, url_prefix='/my/vm')


@mod.route('/test', defaults={'page':1})
@mod.route('/test/page/<int:page>')
def test(page, **kvargs):
    vms = VM.query.filter(and_(VM.user_id==current_user.user_id, VM.if_test==1)).paginate(page, per_page=15, error_out=True)
    return render_template('my/vm/test.html', vms=vms)


@mod.route('/production', defaults={'page':1})
@mod.route('/production/page/<int:page>')
def production(page, **kvargs):
    vms = VM.query.filter(and_(VM.user_id==current_user.user_id, VM.if_test!=1)).paginate(page, per_page=15, error_out=True)
    return render_template('my/vm/production.html', vms=vms)
