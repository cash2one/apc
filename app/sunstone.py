# -*- coding: utf-8 -*-

from app.utils import http_req


class Sunstone:

    def __init__(self, cluster): 
        self.api = cluster.sunstone_api.replace('http://', '')
        cookie_req = http_req(host=self.api, uri='/login', method='POST', headers={"Authorization": cluster.sunstone_auth})
        for x in cookie_req.getheaders():
            if x[0] == "set-cookie":
                cookie = x[1].split(';')[0]
        self.headers = {"Cookie": cookie}

    def vnet(self):
        return http_req(host=self.api, uri='/vnet', headers=self.headers)

    def image(self, method='GET', params=''):
        return http_req(host=self.api, uri='/image', method=method, params=params, headers=self.headers)

    def image_id(self, image_id, method='GET'):
        return http_req(host=self.api, uri=('/image/%s' % image_id), method=method, headers=self.headers)

    def image_action(self, image_id, params, method='POST'):
        return http_req(host=self.api, uri=('/image/%s/action' % image_id), method=method, params=params, headers=self.headers)

    def host(self):
        return http_req(host=self.api, uri='/host', headers=self.headers)

    def datastore(self):
        return http_req(host=self.api, uri='/datastore', headers=self.headers)

    def datastore_id(self, ds_id):
        return http_req(host=self.api, uri=('/datastore/%s' % ds_id), headers=self.headers)

    def vm(self):
        return http_req(host=self.api, uri='/vm', headers=self.headers)

    def vm_id(self, vm_id):
        return http_req(host=self.api, uri=('/vm/%s' % vm_id), headers=self.headers)

    def vm_action(self, vm_id, params):
        return http_req(host=self.api, uri=('/vm/%s/action' % vm_id), method='POST', params=params, headers=self.headers)

    def host(self):
        return http_req(host=self.api, uri='/host', headers=self.headers)
