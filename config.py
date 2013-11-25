# -*- coding: utf8 -*-

# Base config
DEBUG = True
PRD_CONFIG = 'prd.cfg'
SECRET_KEY = '\x9b\xaebt>\x05I\xbb,\x1d\xb1Z\xb0\xc1 \x00\xba\xb2\xc5\x03\r\xf1\x1c\x93'


# DB Config
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_DATABASE_URI = 'mysql://caixh:caixh123@192.168.1.103/apc'


# OAuth Config
AUTH_URL = 'https://auth.corp.anjuke.com'
AUTH_ID = 'apc_dev'
AUTH_SECRET = 'a6f261de'
REQUEST_TOKEN_URL = AUTH_URL + '/authorize.php?client_id=' + AUTH_ID + '&response_type=code'
ACCESS_TOKEN_URL = AUTH_URL + '/token.php?client_id=' + AUTH_ID + '&client_secret=' + AUTH_SECRET + '&grant_type=authorization_code&code=%s'
RESOURCE_URL = AUTH_URL + '/resource.php'
LOGOUT_URL = AUTH_URL + '/logout.php?client_id=' + AUTH_ID + '&client_secret=' + AUTH_SECRET


# User role
ROLE = {
    0: u'普通用户',
    1: u'管理员',
}


# Status Config
ORDER_STATUS = {
    0: {'label':u'审核中',      'class':u'label-info'},
    1: {'label':u'已完成',      'class':u'label-success'},
    2: {'label':u'创建失败',    'class':u'label-important'},
    4: {'label':u'已取消',      'class':u''},
    5: {'label':u'被驳回',      'class':u'label-important'},
}

LCM_STATE = {
    0:  "LCM_INIT",
    1:  "PROLOG",
    2:  "BOOT",
    3:  "RUNNING",
    4:  "MIGRATE",
    5:  "SAVE",
    6:  "SAVE",
    7:  "SAVE",
    8:  "MIGRATE",
    9:  "PROLOG",
    10: "EPILOG",
    11: "EPILOG",
    12: "SHUTDOWN",
    13: "SHUTDOWN",
    14: "FAILURE",
    15: "CLEANUP",
    16: "UNKNOWN",
    17: "HOTPLUG",
    18: "SHUTDOWN",
    19: "BOOT",
    20: "BOOT",
    21: "BOOT",
    22: "BOOT",
    23: "CLEANUP",
    24: "SNAPSHOT",
    25: "HOTPLUG",
    26: "HOTPLUG",
    27: "HOTPLUG",
    28: "HOTPLUG",
    29: "SHUTDOWN",
    30: "EPILOG",
    31: "PROLOG",
    32: "BOOT",
}

VM_STATE = {
    0:  'PENDING',
    1:  'DEPLOYING',
    2:  'RUNNING',
    3:  'UNDEPLOYING',
    4:  'WARNING',
    5:  'DONE',
    6:  'FAILED_UNDEPLOYING',
    7:  'FAILED_DEPLOYING',
    8:  'SCALING',
    9:  'FAILED_SCALING',
    10: 'COOLDOWN',
}


# Price
PRICE = {
    'base': 10,
    'cpu': 50,
    'mem': 20,
    'disk': 0.4,
    'nic': 10,
}
