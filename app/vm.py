# -*- coding: utf-8 -*-

from flask import render_template
from xml.dom import minidom
from sqlalchemy import and_

import time
import simplejson as json

from app import app
from app.models import *
from app.occi import OCCI
from app.sunstone import Sunstone
from app.dicts import *


class VMC():

    def __init__(self):
        pass


    def create(self, order, ds_mad):
        disk_arr = []
        network_dict = network2dict()
        occi = OCCI(order.cluster)
        sunstone = Sunstone(order.cluster)

        # if ceph ds, create datablock first
        posts = '{"image":{"NAME":"%s","TYPE":"DATABLOCK","PERSISTENT":"YES","SIZE":"%s","FSTYPE":"raw"},"ds_id":"%s"}'
        if ds_mad == "ceph":
            for x in order.disk:
                params = posts % (time.time(), x*1024, order.cluster.ds_id)
                resp = sunstone.image(method='POST', params=params)
                resp = json.loads(resp.data)
                disk_arr.append(resp['IMAGE']['ID'])

        ready_tag = False
        while not ready_tag:
            ready_tag = True
            for d in disk_arr:
                resp = sunstone.image_id(d)
                data = json.loads(resp.data)
                if data['IMAGE']['STATE'] != "1":
                    ready_tag = False

        template = render_template('vm/occi_template.html', order=order, network_dict=network_dict, disk_arr=disk_arr)
        resp = occi.compute_create(template)
        if resp.status != 201:
            return 0

        xmldoc = minidom.parseString(resp.data)
        vm_id = xmldoc.getElementsByTagName('ID')[0].firstChild.nodeValue
        hostname = xmldoc.getElementsByTagName('NAME')[0].firstChild.nodeValue
        state = xmldoc.getElementsByTagName('STATE')[0].firstChild.nodeValue
        ip = [a.firstChild.nodeValue for a in xmldoc.getElementsByTagName('IP')]

        posts = '{"action":{"perform":"rename","params":{"name":"%s"}}}'
        if ds_mad == "ceph":
            for index,d in enumerate(disk_arr):
                resp = sunstone.image_action(d, (posts % ("%s-%s" % (vm_id, index+1))))

        try:
            vm = VM(hostname, ip, order.cpu, order.mem, order.network, order.disk, order.desc, order.id, 
                    order.cluster_id, vm_id, state, -1, order.user.id, 0, order.cluster.if_test, order.days)
            db.session.add(vm)
            db.session.commit()
            vminst = VMC()
            vminst.gen_price(vm)
            return 1
        except:
            return 0


    def gen_price(self, vm):
        vminst = VMC()
        price = app.config['PRICE']['base'] + \
                app.config['PRICE']['cpu'] * vm.cpu + \
                app.config['PRICE']['mem'] * vm.mem + \
                app.config['PRICE']['nic'] * vm.network.__len__()
        for x in vm.disk:
            price +=  app.config['PRICE']['disk'] * x
        vm.price = price
        db.session.add(vm)
        db.session.commit()
        return 1


    def rename(self, vm, newname):
        sunstone = Sunstone(vm.order.cluster)
        params = '{"action":{"perform":"rename","params":{"name":"%s"}}}' % newname
        resp = sunstone.vm_action(vm.vm_id, params)
        return 1 if resp.status==204 else 0


    def refresh(self):
        cluster = Cluster.query.all()
        for x in cluster:
            sunstone = Sunstone(x)
            resp = sunstone.vm()
            if resp.status != 200:
                return 0
            info = json.loads(resp.data)['VM_POOL']['VM']
            if type(info) == dict:
                info = [info]
            for y in info:
                vm = VM.query.filter(and_(VM.cluster_id==x.id, VM.vm_id==int(y['ID']))).first()
                if not vm:
                    next
                lcm_state_code = int(y['LCM_STATE'])
                vm_state_code = int(y['STATE'])
                if lcm_state_code == 0:
                    vm.status = app.config['VM_STATE'][vm_state_code]
                else:
                    vm.status = app.config['LCM_STATE'][lcm_state_code]
                db.session.add(x)
                db.session.commit()
        return 1


    def delete(self, vm):
        occi = OCCI(vm.order.cluster)
        sunstone = Sunstone(vm.order.cluster)
        vm_info = json.loads(sunstone.vm_id(vm.vm_id).data)

        resp = occi.compute_delete(vm.vm_id)
        if resp.status != 204:
            return 0

        disk = vm_info['VM']['TEMPLATE']['DISK']
        if type(disk) == dict:
            disk = [disk]
        for x in disk:
            if x['CLONE'] == 'NO':
                sunstone.image_id(image_id=x['IMAGE_ID'], method='DELETE')

        try:
            db.session.delete(vm)
            db.session.commit()
            return 1
        except:
            return 0
        return 1
