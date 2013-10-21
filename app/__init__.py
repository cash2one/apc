# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)


#
# Load config
#
app.config.from_object('config')
app.config.from_pyfile(app.config['PRD_CONFIG'], silent=True)


#
# DB
#
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


#
# Login
#
from flask.ext.login import LoginManager
from app.models import User, UserDB

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = None

@login_manager.user_loader
def load_user(userid):
    userdb = UserDB.query.filter(UserDB.username==userid).first()
    return User(userid, userdb.username, userdb.chinese_name, userdb.email, userdb.role)


#
# Views
#
from app.views import general
from app.views import buy
from app.views import sunstone_api
from app.views.admin import index
from app.views.admin import idc
from app.views.admin import cluster
from app.views.admin import cpu_mem
from app.views.admin import network
from app.views.admin import osimage

app.register_blueprint(buy.mod)
app.register_blueprint(sunstone_api.mod)
app.register_blueprint(index.mod)
app.register_blueprint(idc.mod)
app.register_blueprint(cluster.mod)
app.register_blueprint(cpu_mem.mod)
app.register_blueprint(network.mod)
app.register_blueprint(osimage.mod)
