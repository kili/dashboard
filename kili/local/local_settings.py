import os
from kili.settings import *

KEYSTONE_TOKEN = "3DD7j.2v-N8si0qiT_Uf" 
KEYSTONE_URL = "http://10.186.43.2:35357/v2.0"

BROKER_URL = 'amqp://horizon_dashboard:b:gfLeV5LpU6xljZwSl0@10.186.43.2//horizon_dashboard'
        
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
    
OPENSTACK_HOST = "10.186.43.2"
OPENSTACK_KEYSTONE_URL = "http://{}:5000/v2.0".format(OPENSTACK_HOST)
        
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
COMPRESS_ENABLED = False

DEBUG = True

ENV_NAME = "dev" 

OPENSTACK_SSL_NO_VERIFY = True
