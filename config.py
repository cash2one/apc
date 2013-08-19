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
