# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, render_template
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

        user = User(info['username'], info['username'], info['chinese_name'], info['email'], 0)
        login_user(user)
        return redirect(url_for('.index'))

    return redirect(app.config['REQUEST_TOKEN_URL'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(app.config['LOGOUT_URL'])
