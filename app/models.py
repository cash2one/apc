# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin

from sqlalchemy import *

from app import db


class User(UserMixin):
    def __init__(self, id, username, chinese_name, email, role):
        self.id = id
        self.username = username
        self.chinese_name = chinese_name
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User %r, %r>' % (self.username, self.chinese_name)


class UserDB(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    chinese_name = Column(String(32))
    email = Column(String(64))
    role = Column(Integer)
    ssh_pubkey = Column(Text)

    def __init__(self, username, chinese_name, email, role=0, ssh_pubkey=None):
        self.username = username
        self.chinese_name = chinese_name
        self.email = email
        self.role = role
        self.ssh_pubkey = ssh_pubkey

    def __repr__(self):
        return '<User %r, %r>' % (self.username, self.chinese_name)


class IDC(db.Model):
    __tablename__ = 'idc'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    chinese_name = Column(String(64))
    occi_api = Column(String(256))
    sunstone_api = Column(String(256))
    api_auth = Column(String(256))

    def __init__(self, name, chinese_name, occi_api, sunstone_api, api_auth):
        self.name = name
        self.chinese_name = chinese_name
        self.occi_api = occi_api
        self.sunstone_api = sunstone_api
        self.api_auth = api_auth

    def __repr__(self):
        return '<IDC %r>' % self.name


class CPU_Mem(db.Model):
    __tablename__ = "cpu_mem"
    id = Column(Integer, primary_key=True)
    cpu = Column(Integer)
    mem = Column(Integer)

    def __init__(self, cpu, mem):
        self.cpu = cpu
        self.mem = mem

    def __repr__(self):
        return '<%r Cores %rG>' % (self.cpu, self.mem)


class Network(db.Model):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True)
    idc_id = Column(Integer)
    sunstone_id = Column(Integer)
    sunstone_name = Column(String(256))
    name = Column(String(256))
    if_default = Column(Integer)

    def __init__(self, idc_id, sunstone_id, sunstone_name, name, if_default):
        self.idc_id = idc_id
        self.sunstone_id = sunstone_id
        self.sunstone_name = sunstone_name
        self.name = name
        self.if_default = if_default

    def __repr__(self):
        return '<Network %s>' % self.name


class OS_Image(db.Model):
    __tablename__ = "os_image"
    id = Column(Integer, primary_key=True)
    idc_id = Column(Integer)
    sunstone_id = Column(Integer)
    sunstone_name = Column(String(256))
    name = Column(String(256))
    if_default = Column(Integer)

    def __init__(self, idc_id, sunstone_id, sunstone_name, name, if_default):
        self.idc_id = idc_id
        self.sunstone_id = sunstone_id
        self.sunstone_name = sunstone_name
        self.name = name
        self.if_default = if_default

    def __repr__(self):
        return '<OS %s>' % self.name
