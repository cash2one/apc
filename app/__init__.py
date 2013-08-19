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

app.register_blueprint(buy.mod)
