"""
Django settings for kili project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from kombu import Exchange, Queue

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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_8!hwo0@xfkkz15e%+nh4f0v7ra7)jucipgt9)o(3s16v=^tk%'

from openstack_dashboard.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ 'localhost', ]

# Application definition

INSTALLED_APPS = (
    'openstack_dashboard',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    'openstack_auth',
    'registration',
    'allauth',
    'allauth.account',
    'south',
    'async',
)

MIDDLEWARE_CLASSES = ( 
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'horizon.middleware.HorizonMiddleware',
        'django.middleware.doc.XViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kili.urls'

WSGI_APPLICATION = 'kili.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

DEFAULT_FROM_EMAIL = "Kili <admin@kili.io>"

AUTH_USER_MODEL = 'registration.User'

DEFAULT_ROLES = ["Member",]

SITE_ID = 1

CELERY_DEFAULT_QUEUE = 'registration'
CELERY_QUEUES = ( 
        Queue('registration', Exchange('registration'), routing_key='registration'),
)
CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_PERSISTENT = True

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_SIGNUP_FORM_CLASS = "registration.forms.RegistrationForm"
ACCOUNT_ADAPTER = "registration.adapters.CompanyAdapter"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/" 
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/" 
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 25

EMAIL_CONFIRMATION_REDIRECT = "/horizon"
COMPRESS_OFFLINE = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'HTTPS'

COMPRESS_OFFLINE_CONTEXT = {
        'STATIC_URL': STATIC_URL,
        'HORIZON_CONFIG': HORIZON_CONFIG
}

OPENSTACK_HOST = "10.186.43.2"
OPENSTACK_KEYSTONE_URL = "http://{}:5000/v2.0".format(OPENSTACK_HOST)
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "_member_"

COMPRESS_ENABLED = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

KEYSTONE_TOKEN = "JbztrK_H2,yO0jJ4.Vje"
KEYSTONE_DEFAULT_GROUP = "admin"

#OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True

OPENSTACK_API_VERSION = {
    'identity': 2.0,
    'volume': 2,
}

INSTALLED_APPS = list(INSTALLED_APPS)  # Make sure it's mutable
settings.update_dashboards([
        openstack_dashboard.enabled,
        openstack_dashboard.local.enabled,
], HORIZON_CONFIG, INSTALLED_APPS)

