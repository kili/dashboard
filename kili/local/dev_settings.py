from kili.settings import *  # noqa

KEYSTONE_TOKEN = "HWXvI5jbn3pln5m1u0Iw"
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
HOST = getattr(settings, "HOST", "http://127.0.0.1")

COMMON_INITIAL = { 
    'first_name': 'John',
    'last_name': 'Doe',
    'month': '06',
    'year': '2020',
    'card_type': 'visa',
    'verification_value': '000'
}

GATEWAY_INITIAL = {
    'stripe': {
        'number': '4242424242424242',
    },
}

INTEGRATION_INITIAL = {
    'stripe': {
        'amount': 1,
        'credit_card_number': '4222222222222',
        'credit_card_cvc': '100',
        'credit_card_expiration_month': '01',
        'credit_card_expiration_year': '2020'
    },
}

for k, v in GATEWAY_INITIAL.iteritems():
    v.update(COMMON_INITIAL)

for k, v in INTEGRATION_INITIAL.iteritems():
    v.update(COMMON_INITIAL)


MERCHANT_TEST_MODE = True # Toggle for live
MERCHANT_SETTINGS = { 
    "stripe": {
        "API_KEY": "sk_test_hXpCT9Oqs4PszDOhXK6TY9XS",
        "PUBLISHABLE_KEY": "pk_test_1dOtVgHQSGxzXYHk2ghg5YI1", # Used for stripe integration
        }   
}
