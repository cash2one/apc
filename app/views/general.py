# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, render_template, send_from_directory, make_response, abort
from flask.ext.login import login_required, login_user, logout_user, current_user

from urllib import urlopen, urlencode

import simplejson as json

from app import app, db
from app.models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/initdb')
@login_required
def initdb():
    try:
        db.create_all()
    finally:
        return 'Init DB!'


@app.route('/custom_static/<path:filename>')
def custom_static(filename):
    content_type_dict = {
        'js': 'application/javascript',
        'css': 'text/css',
        'jpg': '',
        'png': 'image/png',
        'gif': '',
    }

    try:
        suffix = filename.split('/')[len(filename.split('/'))-1].split('?')[0].split('.')[1]
        resp = make_response(open('app/templates/' + filename).read())
    except:
       abort(404) 

    if content_type_dict.has_key(suffix):
        resp.headers["Content-type"] = content_type_dict[suffix]
    else:
        resp.headers["Content-type"] = "text/plain"

    return resp


@app.route('/login')
def login():
    if request.args.get('code'):
        return redirect(app.config['ACCESS_TOKEN_URL'] % request.args.get('code'))

    if request.args.get('access_token'):
        try:
            f = urlopen(app.config['RESOURCE_URL'], urlencode({'oauth_token':request.args.get('access_token'), 'getinfo':True}))
            info = json.loads(f.read())
        except:
            return redirect(app.config['REQUEST_TOKEN_URL'])

        if UserDB.query.filter(UserDB.username==info['username']).count() <= 0:
            userdb = UserDB(info['username'], info['chinese_name'], info['email'])
            db.session.add(userdb)
            db.session.commit()

        user_id = UserDB.query.filter(UserDB.username==info['username']).first().id
        user = User(info['username'], user_id, info['username'], info['chinese_name'], info['email'], 0)
        login_user(user)
        return redirect(url_for('.index'))

    return redirect(app.config['REQUEST_TOKEN_URL'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(app.config['LOGOUT_URL'])
