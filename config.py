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
     0: "LCM_INIT",
     1: "PROLOG",
     2: "BOOT",
     3: "RUNNING",
     4: "MIGRATE",
     5: "SAVE_STOP",
     6: "SAVE_SUSPEND",
     7: "SAVE_MIGRATE",
     8: "PROLOG_MIGRATE",
     9: "PROLOG_RESUME",
    10: "EPILOG_STOP",
    11: "EPILOG",
    12: "SHUTDOWN",
    13: "CANCEL",
    14: "FAILURE",
    15: "CLEANUP_RESUBMIT",
    16: "UNKNOWN",
    17: "HOTPLUG",
    18: "SHUTDOWN_POWEROFF",
    19: "BOOT_UNKNOWN",
    20: "BOOT_POWEROFF",
    21: "BOOT_SUSPENDED",
    22: "BOOT_STOPPED",
    23: "CLEANUP_DELETE",
    24: "HOTPLUG_SNAPSHOT",
    25: "HOTPLUG_NIC",
    26: "HOTPLUG_SAVEAS",
    27: "HOTPLUG_SAVEAS_POWEROFF",
    28: "HOTPLUG_SAVEAS_SUSPENDED",
}

VM_STATE = {
    0:  "INIT",
    1: "PENDING",
    2:  "HOLD",
    3:  "ACTIVE",
    4:  "STOPPED",
    5:  "SUSPENDED",
    6:  "DONE",
    7:  "FAILED",
    8:  "POWEROFF",
}


# Price
PRICE = {
    'base': 10,
    'cpu': 50,
    'mem': 20,
    'disk': 0.4,
    'nic': 10,
}
