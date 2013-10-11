# -*- coding: utf-8 -*-

from app.models import *


def idc2dict():
    ret = {}

    for i in IDC.query.all():
        ret[i.id] = i

    return ret


def network2dict():
    ret = {}
    
    for n in Network.query.all():
        ret[n.id] = n

    return ret
