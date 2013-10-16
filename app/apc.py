# -*- coding: utf-8 -*-

import simplejson as json

from app.sunstone import Sunstone
from app.models import *


class APC:

    def __init__(self, idc):
        self.idc = idc


    def vnet_sunstone(self):
        ret = []

        sunstone = Sunstone(self.idc)
        data = json.loads(sunstone.vnet().data)

        for vnet in data['VNET_POOL']['VNET']:
            ele = {}
            ele['sunstone_id'] = int(vnet['ID'])
            ele['sunstone_name'] = vnet['NAME']
            ret.append(ele)

        return ret


    def image_sunstone(self):
        ret = []

        sunstone = Sunstone(self.idc)
        data = json.loads(sunstone.image().data)

        for image in data['IMAGE_POOL']['IMAGE']:
            ele = {}
            ele['sunstone_id'] = int(image['ID'])
            ele['sunstone_name'] = image['NAME']
            ret.append(ele)

        return ret
