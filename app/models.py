# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import TypeDecorator, UnicodeText

import datetime

from app import db


class ArrInt(TypeDecorator):
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if type(value) is list:
            value = ','.join([str(a) for a in value])
        return value

    def process_result_value(self, value, dialect):
        if value != '':
            value = [int(a) for a in value.split(',')]
        else:
            value = []

        return value


class ArrStr(TypeDecorator):
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if type(value) is list:
            value = ','.join([str(a) for a in value])
        return value

    def process_result_value(self, value, dialect):
        if value != '':
            value = value.split(',')
        else:
            value = []

        return value


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
    if_test = Column(Integer)
    host = Column(String(64))
    occi_api = Column(String(256))
    occi_auth = Column(String(256))
    sunstone_api = Column(String(256))
    sunstone_auth = Column(String(256))
    ds_id = Column(Integer)
    ds_name = Column(String(256))

    idc = relationship("IDC")
    #os_images = relationship("os_image", backref="cluster")

    def __init__(self, idc_id, name, if_test, host, occi_api, occi_auth, sunstone_api, sunstone_auth, ds_id, ds_name):
        self.idc_id = idc_id
        self.name = name
        self.if_test = if_test
        self.host = host
        self.occi_api = occi_api
        self.occi_auth = occi_auth
        self.sunstone_api = sunstone_api
        self.sunstone_auth = sunstone_auth
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

    cluster = relationship('Cluster', backref=backref('network', order_by=id))

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

    cluster = relationship('Cluster', backref=backref('os_image', order_by=id))

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
    network = Column(ArrInt())
    disk = Column(ArrInt())
    os_id = Column(Integer, ForeignKey('os_image.id'))
    cnt = Column(Integer)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    desc = Column(String(256))
    days = Column(Integer)
    created_time = Column(DateTime, default=datetime.datetime.now)

    cluster = relationship("Cluster")
    user = relationship("UserDB")
    os = relationship("OS_Image")
    vm = relationship("VM")

    def __init__(self, cluster_id, cpu, mem, network, disk, os_id, cnt, status, user_id, desc, days):
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
        self.days = days

    def __repr__(self):
        return '<Order %s>' % self.desc


class VM(db.Model):
    __tablename__ = "vm"
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64))
    ip = Column(ArrStr())
    cpu = Column(Integer)
    mem = Column(Integer)
    network = Column(ArrInt())
    disk = Column(ArrInt())
    desc = Column(String(256))
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    cluster_id = Column(Integer, ForeignKey('cluster.id'), nullable=False)
    vm_id = Column(Integer)
    status = Column(String(64))
    zeus_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price = Column(Float)
    if_test = Column(Integer)
    days = Column(Integer)
    created_time = Column(DateTime, default=datetime.datetime.now)

    order = relationship("Orders")
    cluster = relationship("Cluster")
    user = relationship("UserDB")

    def __init__(self, hostname, ip, cpu, mem, network, disk, desc, order_id, 
                 cluster_id, vm_id, status, zeus_id, user_id, price, if_test, days):
        self.hostname = hostname
        self.ip = ip
        self.cpu = cpu
        self.mem = mem
        self.network = network
        self.disk = disk
        self.desc = desc
        self.order_id = order_id
        self.cluster_id = cluster_id
        self.vm_id = vm_id
        self.status = status
        self.zeus_id = zeus_id
        self.user_id = user_id
        self.price = price
        self.if_test = if_test
        self.days = days

    def __repr__(self):
        return '<VM %s>' % self.hostname


class Hosts(db.Model):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey('cluster.id'), nullable=False)
    sunstone_id = Column(Integer)
    hostname = Column(String(64))
    vmnum = Column(Integer)
    max_cpu = Column(Integer)
    cpu_usage = Column(Integer)
    used_cpu = Column(Integer)
    max_mem = Column(Integer)
    mem_usage = Column(Integer)
    used_mem = Column(Integer)
    last_update_time = Column(Integer)

    cluster = relationship("Cluster")

    def __init__(self, cluster_id, sunstone_id, hostname, vmnum, max_cpu, cpu_usage, used_cpu,
                 max_mem, mem_usage, used_mem, last_update_time):
        self.cluster_id = cluster_id
        self.sunstone_id = sunstone_id
        self.hostname = hostname
        self.vmnum = vmnum
        self.max_cpu = max_cpu
        self.cpu_usage = cpu_usage
        self.used_cpu = used_cpu
        self.max_mem = max_mem
        self.mem_usage = mem_usage
        self.used_mem = used_mem
        self.last_update_time = last_update_time

    def __repr__(self):
        return '<Host %s>' % self.hostname
