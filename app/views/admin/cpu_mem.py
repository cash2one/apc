# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify
from wtforms import Form, BooleanField, TextField, validators
from operator import itemgetter, attrgetter

from app import app, db
from app.models import *

mod = Blueprint('cpu_mem', __name__, url_prefix='/admin/cpu_mem')


@mod.route('/', methods=['GET'])
def index():
    rows = CPU_Mem.query.all()
    return render_template('admin/cpu_mem/index.html', rows=rows)


@mod.route('/add/', methods=['POST'])
def add():
    cpu = request.form["cpu"]
    mem = request.form["mem"]
    if not cpu.isdigit():
        return jsonify(msg="cpu need be digit")
    if not mem.isdigit():
        return jsonify(msg="mem need be digit")
    if CPU_Mem.query.filter_by(cpu=cpu,mem=mem).count():
        return jsonify(msg="existed");
    c_m = CPU_Mem(cpu, mem)
    db.session.add(c_m)
    db.session.commit()
    return jsonify(id=c_m.id)


@mod.route('/update/', methods=['POST'])
def update():
    id = request.form["id"]
    cpu = request.form["cpu"]
    mem = request.form["mem"]
    if not cpu.isdigit():
        return jsonify(msg="cpu need be digit")
    if not mem.isdigit():
        return jsonify(msg="mem need be digit")
    if CPU_Mem.query.filter_by(cpu=cpu,mem=mem).count():
        return jsonify(msg="existed");
    c_m = CPU_Mem.query.get(id)
    c_m.cpu = cpu
    c_m.mem = mem
    db.session.commit()
    return jsonify(flag=1)


@mod.route('/delete/', methods=['POST'])
def delete():
    id = request.form["id"]
    c_m = CPU_Mem.query.get(id)
    db.session.delete(c_m)
    db.session.commit()
    return jsonify(flag=1)
