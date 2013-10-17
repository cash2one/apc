# -*- coding: utf-8 -*-

import httplib, urllib


def http_req(host, uri, method='GET', params='', headers=''):
    ret = {}

    params = urllib.urlencode(params)
    conn = httplib.HTTPConnection(host)
    conn.request(method, uri, params, headers)
    resp = conn.getresponse()
    resp.data = resp.read()

    return resp


def get_form_errors(form):
    arr = [' '.join(form.errors[k]) for k in form.errors.keys()]
    msg = ' '.join(arr)
    return msg
