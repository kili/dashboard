import os
from kili.settings import *

KEYSTONE_TOKEN = "JbztrK_H2,yO0jJ4.Vje"
KEYSTONE_URL = "http://10.186.43.2:35357/v2.0"

BROKER_URL = 'amqp://horizon_dashboard:iamapassword@127.0.0.1//horizon_dashboard'
        
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'horizon_dashboard',
        'USER': 'horizon',
        'PASSWORD': 'vSzjLZT3YmdzNL1k7OuJ',
        'HOST': '10.186.43.2',
        'PORT': '3306',
    },
}   

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = ( '127.0.0.1', )

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

OPENSTACK_HOST = "10.186.43.2"
OPENSTACK_KEYSTONE_URL = "http://{}:5000/v2.0".format(OPENSTACK_HOST)
        
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
COMPRESS_ENABLED = False

DEBUG = True

ENV_NAME = "dev" 

DEBUG_TOOLBAR_PATCH_SETTINGS = False
