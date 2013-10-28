# -*- coding: utf-8 -*-

from app.models import *


def network2dict():
    ret = {}
    for n in Network.query.all():
        ret[n.id] = n
    return ret


def osimage2dict():
    ret = {}
    for o in OS_Image.query.all():
        ret[o.id] = o
    return ret
