# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request,jsonify
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required, length

from app.models import *

mod = Blueprint('idc', __name__, url_prefix='/admin/idc')

from app.models import IDC
from app import db

@mod.route('/index')
@mod.route('/')
def index():
    form = IdcForm()
    allRes = IDC.query.all()
    print allRes
    return render_template('admin/idc/index.html', form=form, allRes=allRes)

@mod.route('/add/', methods=['GET', 'POST'])
def add():
    name = request.args.get('name')
    cname = request.args.get('cname')
    occapi = request.args.get('occapi')
    sunapi = request.args.get('sunapi')

    try:
        idc = IDC(name, cname, occapi, sunapi)
        db.session.add(idc)
        db.session.commit()
    except:
        print "except"
        
    return jsonify(id = idc.id, 
                   name = idc.name,
                   cname = idc.chinese_name,
                   occapi = idc.occi_api,
                   sunapi = idc.sunstone_api)

@mod.route('/edit/', methods=['GET', 'POST'])
def edit():
    id = request.args.get('id')
    name = request.args.get('name')
    cname = request.args.get('cname')
    occapi = request.args.get('occapi')
    sunapi = request.args.get('sunapi')

    try:
        idc = IDC.query.get(id)
        idc.name = name
        idc.chinese_name = cname
        idc.occi_api = occapi
        idc.sunstone_api = sunapi
        db.session.commit()
    except:
        print "except"     
    return "success!"

@mod.route('/delete/', methods=['GET', '[POST'])
def delete():
    id = request.args.get('id')  

    try:
        idc = IDC.query.get(id)
        db.session.delete(idc)
        db.session.commit()
    except:
        print "except"
    return 'success!'


class IdcForm(Form):
    name = TextField(u'name', validators = [Required(), length(max=20)])
    cname = TextField(u'cname', validators = [Required(), length(max=20)])
    occapi = TextField(u'occiapi', validators = [Required(), length(max=20)])
    sunapi = TextField(u'sunapi', validators = [Required(), length(max=20)])
