# -*- coding: utf-8 -*-

from app.utils import http_req


class Sunstone:

    def __init__(self, cluster): 
        self.api = cluster.sunstone_api.replace('http://', '')
        self.headers = {"Cookie": cluster.api_auth}

    def vnet(self):
        return http_req(host=self.api, uri='/vnet', headers=self.headers)

    def image(self):
        return http_req(host=self.api, uri='/image', headers=self.headers)

    def host(self):
        return http_req(host=self.api, uri='/host', headers=self.headers)

    def datastore(self):
        return http_req(host=self.api, uri='/datastore', headers=self.headers)
