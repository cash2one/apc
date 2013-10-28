# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin

from sqlalchemy import *
from sqlalchemy.orm import relationship

import datetime

from app import db


class User(UserMixin):
    def __init__(self, id, user_id, username, chinese_name, email, role):
        self.id = id
        self.user_id = user_id
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

    def __init__(self, name, chinese_name):
        self.name = name
        self.chinese_name = chinese_name

    def __repr__(self):
        return '<IDC %r>' % self.name


class Cluster(db.Model):
    __tablename__ = 'cluster'
    id = Column(Integer, primary_key=True)
    idc_id = Column(Integer, ForeignKey('idc.id'))
    name = Column(String(64))
    host = Column(String(64))
    occi_api = Column(String(256))
    sunstone_api = Column(String(256))
    api_auth = Column(String(256))
    ds_id = Column(Integer)
    ds_name = Column(String(256))

    idc = relationship("IDC")

    def __init__(self, idc_id, name, host, occi_api, sunstone_api, api_auth, ds_id, ds_name):
        self.idc_id = idc_id
        self.name = name
        self.host = host
        self.occi_api = occi_api
        self.sunstone_api = sunstone_api
        self.api_auth = api_auth
        self.ds_id = ds_id
        self.ds_name = ds_name

    def __repr__(self):
        return '<Cluster %r>' % self.name


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
    cluster_id = Column(Integer, ForeignKey('cluster.id'))
    sunstone_id = Column(Integer)
    sunstone_name = Column(String(256))
    name = Column(String(256))
    if_default = Column(Integer)

    cluster = relationship('Cluster')

    def __init__(self, cluster_id, sunstone_id, sunstone_name, name, if_default):
        self.cluster_id = cluster_id
        self.sunstone_id = sunstone_id
        self.sunstone_name = sunstone_name
        self.name = name
        self.if_default = if_default

    def __repr__(self):
        return '<Network %s>' % self.name


class OS_Image(db.Model):
    __tablename__ = "os_image"
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey('cluster.id'))
    sunstone_id = Column(Integer)
    sunstone_name = Column(String(256))
    name = Column(String(256))
    if_default = Column(Integer)

    cluster = relationship('Cluster')

    def __init__(self, cluster_id, sunstone_id, sunstone_name, name, if_default):
        self.cluster_id = cluster_id
        self.sunstone_id = sunstone_id
        self.sunstone_name = sunstone_name
        self.name = name
        self.if_default = if_default

    def __repr__(self):
        return '<OS %s>' % self.name


class Orders(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey('cluster.id'), nullable=False)
    cpu = Column(Integer)
    mem = Column(Integer)
    network = Column(String(256))
    disk = Column(String(256))
    os_id = Column(Integer, ForeignKey('os_image.id'))
    cnt = Column(Integer)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    desc = Column(String(256))
    created_time = Column(DateTime, default=datetime.datetime.now)

    cluster = relationship("Cluster", )
    user = relationship("UserDB")
    os = relationship("OS_Image")

    def __init__(self, cluster_id, cpu, mem, network, disk, os_id, cnt, status, user_id, desc):
        self.cluster_id = cluster_id
        self.cpu = cpu
        self.mem = mem
        self.network = network
        self.disk = disk
        self.os_id = os_id
        self.cnt = cnt
        self.status = status
        self.user_id = user_id
        self.desc = desc

    def __repr__(self):
        return '<Order %s>' % self.desc
