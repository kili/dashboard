from kili.settings import *  # noqa

KEYSTONE_TOKEN = "5zoNv.aryGlnlXu7,oZM"
KEYSTONE_URL = "http://10.0.1.223:35357/v2.0"

BROKER_URL = \
    'amqp://horizon_dashboard:iamapassword@127.0.0.1//horizon_dashboard'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'horizon_dashboard',
        'USER': 'horizon',
        'PASSWORD': '8JN7lebKW.EbGYrYSGwe',
        'HOST': '10.0.1.222',
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

OPENSTACK_HOST = "10.0.1.222"
OPENSTACK_KEYSTONE_URL = "http://{}:5000/v2.0".format(OPENSTACK_HOST)

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
    'os_auth_url': 'http://10.0.1.223/keystone/v2.0'}
