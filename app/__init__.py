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
    return User(userid, userdb.id, userdb.username, userdb.chinese_name, userdb.email, userdb.role)


#
# Views
#
from app.views import general
from app.views import order
from app.views import api
from app.views import sunstone_api
from app.views import vm
from app.views import hosts
from app.views.admin import index as admin_index
from app.views.admin import idc
from app.views.admin import cluster
from app.views.admin import cpu_mem
from app.views.admin import network
from app.views.admin import osimage
from app.views.my import vm as my_vm
from app.views.my import order as my_order

app.register_blueprint(order.mod)
app.register_blueprint(api.mod)
app.register_blueprint(sunstone_api.mod)
app.register_blueprint(vm.mod)
app.register_blueprint(hosts.mod)
app.register_blueprint(admin_index.mod)
app.register_blueprint(idc.mod)
app.register_blueprint(cluster.mod)
app.register_blueprint(cpu_mem.mod)
app.register_blueprint(network.mod)
app.register_blueprint(osimage.mod)
app.register_blueprint(my_vm.mod)
app.register_blueprint(my_order.mod)
