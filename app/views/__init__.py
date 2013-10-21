# -*- coding: utf-8 -*-

from functools import wraps

from app.models import *


#
# Check and load
#
def check_load_idc(func):
    @wraps(func)
    def wrapper(**kvargs):
        idc = IDC.query.get_or_404(kvargs['idc_id'])
        return func(idc=idc, **kvargs)
    return wrapper

def check_load_cluster(func):
    @wraps(func)
    def wrapper(**kvargs):
        cluster = Cluster.query.get_or_404(kvargs['cluster_id'])
        return func(cluster=cluster, **kvargs)
    return wrapper

def check_load_network(func):
    @wraps(func)
    def wrapper(**kvargs):
        network = Network.query.get_or_404(kvargs['network_id'])
        return func(network=network, **kvargs)
    return wrapper

def check_load_osimage(func):
    @wraps(func)
    def wrapper(**kvargs):
        osimage = OS_Image.query.get_or_404(kvargs['osimage_id'])
        return func(osimage=osimage, **kvargs)
    return wrapper

def check_load_cpumem(func):
    @wraps(func)
    def wrapper(**kvargs):
        cpumem = CPU_Mem.query.get_or_404(kvargs['cpumem_id'])
        return func(cpumem=cpumem, **kvargs)
    return wrapper
