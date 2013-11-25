# -*- coding: utf-8 -*-

from app.utils import http_req


class OCCI:

    def __init__(self, cluster):
        self.api = cluster.occi_api.replace('http://', '')
        self.headers = {"Authorization": cluster.occi_auth}

    def compute_create(self, template):
        return http_req(host=self.api, uri='/compute', method='POST', params=template, headers=self.headers)

    def compute_delete(self, id):
        return http_req(host=self.api, uri=('/compute/%s' % id), method='DELETE', headers=self.headers)
