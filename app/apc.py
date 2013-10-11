# -*- coding: utf-8 -*-

import simplejson as json

from app.sunstone import Sunstone
from app.models import *


class APC:

    def __init__(self):
        pass


    def vnet_sunstone(self):
        ret = []

        for idc in IDC.query.all():
            sunstone = Sunstone(idc)
            data = json.loads(sunstone.vnet().data)

            for vnet in data['VNET_POOL']['VNET']:
                ele = {}
                ele['idc_id'] = int(idc.id)
                ele['idc_name'] = str(idc.name)
                ele['sunstone_id'] = int(vnet['ID'])
                ele['sunstone_name'] = vnet['NAME']
                ret.append(ele)

        return ret


    def image_sunstone(self):
        ret = []

        for idc in IDC.query.all():
            sunstone = Sunstone(idc)
            data = json.loads(sunstone.image().data)

            for image in data['IMAGE_POOL']['IMAGE']:
                ele = {}
                ele['idc_id'] = int(idc.id)
                ele['idc_name'] = str(idc.name)
                ele['sunstone_id'] = int(image['ID'])
                ele['sunstone_name'] = image['NAME']
                ret.append(ele)

        return ret
