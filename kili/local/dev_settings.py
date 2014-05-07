from kili.settings import *  # noqa

KEYSTONE_TOKEN = "HWXvI5jbn3pln5m1u0Iw"
KEYSTONE_URL = "http://10.0.1.222:35357/v2.0"

BROKER_URL = \
    'amqp://horizon_dashboard:iamapassword@127.0.0.1//horizon_dashboard'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'horizon_dashboard',
        'USER': 'horizon',
        'PASSWORD': 'vSzjLZT3YmdzNL1k7OuJ',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = ('127.0.0.1', )

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

OPENSTACK_HOST = "10.0.1.223"
OPENSTACK_KEYSTONE_URL = "http://{}:80/keystone/v2.0".format(OPENSTACK_HOST)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COMPRESS_ENABLED = False

DEBUG = True

ENV_NAME = "dev"

DEBUG_TOOLBAR_PATCH_SETTINGS = False

OPENSTACK_SSL_NO_VERIFY = True
