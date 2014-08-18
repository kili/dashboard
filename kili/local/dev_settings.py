from kili.settings import *  # noqa

KEYSTONE_TOKEN = "5zoNv.aryGlnlXu7,oZM"

OPENSTACK_HOST = "10.0.1.222"
#OPENSTACK_HOST = "10.186.43.12"
OPENSTACK_KEYSTONE_URL = "http://{}:5000/v2.0".format(OPENSTACK_HOST)

KEYSTONE_URL = "http://{}:35357/v2.0".format(OPENSTACK_HOST)

BROKER_URL = 'amqp://horizon_dashboard:dfTnELW4d0.-hjFJmb4C@'\
             '{}//horizon_dashboard'.format(OPENSTACK_HOST)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'horizon_dashboard',
        'USER': 'horizon',
        'PASSWORD': '9B_Gt-IvDEWC7HYBpAou',
        'HOST': OPENSTACK_HOST,
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


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COMPRESS_ENABLED = False

DEBUG = True

ENV_NAME = "dev"

DEBUG_TOOLBAR_PATCH_SETTINGS = False

OPENSTACK_SSL_NO_VERIFY = True

# MERCHANT SETTINGS

MERCHANT_TEST_MODE = True  # Toggle for live
MERCHANT_SETTINGS = {
    "stripe": {
        "API_KEY": "sk_test_B6lIS1GVOAL8SenO3DeLlCQN",
        "PUBLISHABLE_KEY": "pk_test_GV1PYwn9wFTVQ0yHyVEWT6Ib",
    }
}

CEILOMETER_AUTH_DATA = {
    'os_username': 'ceilometer',
    'os_password': 'imwUsoT8uNy2UgRwTD7k',
    'os_tenant_name': 'service',
    'os_auth_url': 'http://10.0.1.223/keystone/v2.0'.format(OPENSTACK_HOST)}

K2_API_KEY = '1234567890'
K2_KES_USD_RATE = 88

KOPOKOPO_USERNAME = 'NDPmdiSvwCfj@k2'
KOPOKOPO_PASSWORD = '*4v6"Va&]h^q,QBb=I'
