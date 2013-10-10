# -*- coding: utf-8 -*-

from functools import wraps

from app.models import *


#
# Check and load
#
def check_load_network(func):
    @wraps(func)
    def wrapper(**kvargs):
        network = Network.query.get_or_404(kvargs['network_id'])
        return func(network=network, **kvargs)
    return wrapper
