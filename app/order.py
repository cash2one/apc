# -*- coding: utf-8 -*-

from flask import render_template

import simplejson as json
import time

from app import app
from app.occi import OCCI
from app.sunstone import Sunstone
from app.vm import VMC
from app.models import *
from app.dicts import *


class OrderC():

    def __init__(self, order):
        self.order = order


    def create_vm(self):
        '''
        return
          0: created failed
          1: created succeed
          2: aleady created
        '''
        network_dict = network2dict()
        occi = OCCI(self.order.cluster)
        sunstone = Sunstone(self.order.cluster)
        vminst = VMC()

        # if aleady created
        if self.order.cnt <= self.order.vm.__len__():
            return 2

        ds_info = sunstone.datastore_id(self.order.cluster.ds_id).data
        ds_mad = json.loads(ds_info)['DATASTORE']['DS_MAD']

        # create vm
        ret = 1
        for i in range(0, self.order.cnt - self.order.vm.__len__()):
            if not vminst.create(self.order, ds_mad):
                ret = 0

        if ret:
            self.order.status = 1
        else:
            self.order.status = 2

        db.session.add(self.order)
        db.session.commit()

        return ret


    def cancle(self):
        self.order.status = 4
        db.session.add(self.order)
        db.session.commit()
        # send notify mail

        return 1


    def reject(self):
        self.order.status = 5
        db.session.add(self.order)
        db.session.commit()
        # send notify mail

        return 1
