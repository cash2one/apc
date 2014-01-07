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
        if ds_mad == "ceph":
            ready_tag = False
            posts = '{"image":{"NAME":"%s","TYPE":"DATABLOCK","PERSISTENT":"YES","SIZE":"%s","FSTYPE":"raw"},"ds_id":"%s"}'
            for x in order.disk:
                params = posts % (time.time(), x*1024, order.cluster.ds_id)
                resp = sunstone.image(method='POST', params=params)
                resp = json.loads(resp.data)
                disk_arr.append(resp['IMAGE']['ID'])

            while not ready_tag:
                ready_tag = True
                for x in disk_arr:
                    resp = sunstone.image_id(x)
                    data = json.loads(resp.data)
                    if data['IMAGE']['STATE'] != "1":
                        ready_tag = False

        # create vm
        template = render_template('vm/occi_template.html', order=order, network_dict=network_dict, disk_arr=disk_arr, ds_mad=ds_mad)
        resp = occi.compute_create(template)
        if resp.status != 201:
            return 0

        xmldoc = minidom.parseString(resp.data)
        vm_id = xmldoc.getElementsByTagName('ID')[0].firstChild.nodeValue
        hostname = xmldoc.getElementsByTagName('NAME')[0].firstChild.nodeValue
        state = xmldoc.getElementsByTagName('STATE')[0].firstChild.nodeValue
        ip = [a.firstChild.nodeValue for a in xmldoc.getElementsByTagName('IP')]

        # rename ceph disk
        if ds_mad == "ceph":
            posts = '{"action":{"perform":"rename","params":{"name":"%s"}}}'
            for index,d in enumerate(disk_arr):
                resp = sunstone.image_action(d, (posts % ("%s-%s" % (vm_id, index+1))))

        # write vm info to db
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


    def detail(self, vm):
        ret = {}
        sunstone = Sunstone(vm.cluster)
        resp = sunstone.vm_id(vm.vm_id)
        info = json.loads(resp.data)['VM']

        nic      = info['TEMPLATE'].has_key('NIC') and info['TEMPLATE']['NIC'] or []
        disk     = info['TEMPLATE'].has_key('DISK') and info['TEMPLATE']['DISK'] or []
        snapshot = info['TEMPLATE'].has_key('SNAPSHOT') and info['TEMPLATE']['SNAPSHOT'] or []

        nic      = type(nic)==dict and [nic] or nic
        disk     = type(disk)==dict and [disk] or disk
        snapshot = type(snapshot)==dict and [snapshot] or snapshot

        ret['NIC'] = nic
        ret['DISK'] = disk
        ret['SNAPSHOT'] = snapshot

        return ret


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
        sunstone = Sunstone(vm.cluster)
        params = '{"action":{"perform":"rename","params":{"name":"%s"}}}' % newname
        resp = sunstone.vm_action(vm.vm_id, params)
        return resp.status==204 and 1 or 0


    def resize(self, vm, cpu, mem):
        (cpu, mem) = (int(cpu), int(mem))
        sunstone = Sunstone(vm.cluster)
        params = '{"action":{"perform":"resize","params":{"vm_template":{"CPU":"%s","MEMORY":"%s"},"enforce":false}}}' % (cpu, mem*1024)
        resp = sunstone.vm_action(vm.vm_id, params)
        if resp.status == 204:
            vm.cpu = cpu
            vm.mem = mem
            db.session.add(vm)
            db.session.commit()
            vminst = VMC()
            vminst.gen_price(vm)
            return 1
        else:
            return 0


    def attach_nic(self, vm, network_id):
        sunstone = Sunstone(vm.cluster)
        network = Network.query.get(network_id)
        params = '{"action":{"perform":"attachnic","params":{"nic_template":{"NIC":{"NETWORK":"%s","NETWORK_UNAME":"oneadmin","MODEL":"virtio"}}}}}' % \
                  network.sunstone_name
        resp = sunstone.vm_action(vm.vm_id, params)
        return resp.status==204 and 1 or 0


    def detach_nic(self, vm, nic_id):
        sunstone = Sunstone(vm.cluster)
        params = '{"action":{"perform":"detachnic","params":{"nic_id":"%s"}}}' % nic_id
        resp = sunstone.vm_action(vm.vm_id, params)
        return resp.status==204 and 1 or 0


    def refresh(self):
        cluster = Cluster.query.all()
        for x in cluster:
            sunstone = Sunstone(x)
            resp = sunstone.vm()
            if resp.status != 200:
                return 0
            try:
                info = json.loads(resp.data)['VM_POOL']['VM']
            except:
                return 1
            info = type(info)==dict and [info] or info
            for y in info:
                vm = VM.query.filter(and_(VM.cluster_id==x.id, VM.vm_id==int(y['ID']))).first()
                if not vm:
                    continue
                #IP
                nics = y['TEMPLATE'].has_key('NIC') and y['TEMPLATE']['NIC'] or []
                nics = type(nics)==dict and [nics] or nics
                ip = [z['IP'] for z in nics]
                vm.ip = ' '.join(ip)
                #Status
                lcm_state_code = int(y['LCM_STATE'])
                vm_state_code = int(y['STATE'])
                if lcm_state_code == 0:
                    vm.status = app.config['VM_STATE'][vm_state_code]
                else:
                    vm.status = app.config['LCM_STATE'][lcm_state_code]

                db.session.add(vm)
                db.session.commit()
        return 1


    def start(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"resume"}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def poweroff(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"poweroff","params":{"hard":false}}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def poweroff_hard(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"poweroff","params":{"hard":true}}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def reboot(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"reboot"}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def reboot_hard(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"reset"}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def recreate(self, vm):
        sunstone = Sunstone(vm.cluster)
        post = '{"action":{"perform":"resubmit"}}'
        resp = sunstone.vm_action(vm.vm_id, post)
        return resp.status==204 and 1 or 0


    def delete(self, vm):
        occi = OCCI(vm.cluster)
        sunstone = Sunstone(vm.cluster)
        vm_info = json.loads(sunstone.vm_id(vm.vm_id).data)

        resp = occi.compute_delete(vm.vm_id)
        if resp.status != 204:
            return 0

        disk = 'DISK' in vm_info['VM']['TEMPLATE'] and vm_info['VM']['TEMPLATE']['DISK'] or []
        if type(disk) == dict:
            disk = [disk]
        for x in disk:
            if "CLONE" in x and x['CLONE'] == 'NO':
                sunstone.image_id(image_id=x['IMAGE_ID'], method='DELETE')

        try:
            db.session.delete(vm)
            db.session.commit()
            return 1
        except:
            return 0
