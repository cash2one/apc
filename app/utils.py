# -*- coding: utf-8 -*-

from flask import render_template

import httplib, urllib
import paramiko


def http_req(host, uri, method='GET', params='', headers=''):
    ret = {}

    conn = httplib.HTTPConnection(host)
    conn.request(method, uri, params, headers)
    resp = conn.getresponse()
    resp.data = resp.read()

    return resp


def get_form_errors(form):
    arr = [' '.join(form.errors[k]) for k in form.errors.keys()]
    msg = ' '.join(arr)
    return msg


def ssh_cmd(user, host, cmd):
    ret = {}

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, user, timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)

    ret['exitcode'] = stdout.channel.recv_exit_status()
    ret['stderr'] = stderr.readlines()
    ret['stdout'] = stdout.readlines()

    ssh.close()
    return ret
