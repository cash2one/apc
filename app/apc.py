# -*- coding: utf-8 -*-

import simplejson as json

from app.sunstone import Sunstone
from app.models import *


class APC:

    def __init__(self, cluster):
        self.cluster = cluster


    def vnet_sunstone(self):
        ret = []

        sunstone = Sunstone(self.cluster)
        data = json.loads(sunstone.vnet().data)
        vnets = data['VNET_POOL']['VNET']

        if type(vnets) == dict:
            vnets = [vnets]

        for vnet in vnets:
            ele = {}
            ele['sunstone_id'] = int(vnet['ID'])
            ele['sunstone_name'] = vnet['NAME']
            ret.append(ele)

        return ret


    def image_sunstone(self):
        ret = []

        sunstone = Sunstone(self.cluster)
        data = json.loads(sunstone.image().data)
        images = data['IMAGE_POOL']['IMAGE']

        if type(images) == dict:
            images = [images]

        for image in images:
            ele = {}
            ele['sunstone_id'] = int(image['ID'])
            ele['sunstone_name'] = image['NAME']
            ret.append(ele)

        return ret


    def datastore_sunstone(self):
        ret = []

        sunstone = Sunstone(self.cluster)
        data = json.loads(sunstone.datastore().data)
        datastores = data['DATASTORE_POOL']['DATASTORE']

        if type(datastores) == dict:
            datastores = [datastores]

        for datastore in datastores:
            ele = {}
            ele['sunstone_id'] = int(datastore['ID'])
            ele['sunstone_name'] = datastore['NAME']
            ret.append(ele)

        return ret
