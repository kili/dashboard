from kili.local.dev_settings import *  # noqa


OPENSTACK_HOST = "10.186.43.12"
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

CEILOMETER_AUTH_DATA = {
    'os_username': 'ceilometer',
    'os_password': 'imwUsoT8uNy2UgRwTD7k',
    'os_tenant_name': 'service',
    'os_auth_url': 'http://10.0.1.223/keystone/v2.0'.format(OPENSTACK_HOST)}
