"""
Django settings for kili project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from openstack_dashboard import exceptions
import openstack_dashboard.enabled
import openstack_dashboard.local.enabled
from openstack_dashboard.utils import settings
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

HORIZON_CONFIG = {
    'dashboards': ('project', 'admin', 'settings', 'router',),
    'default_dashboard': 'project',
    'user_home': 'openstack_dashboard.views.get_user_home',
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "http://docs.openstack.org",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.abspath(os.path.join(ROOT_PATH, '..', 'bin'))

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_BRANDING = 'OpenStack Dashboard'

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
# LOGIN_REDIRECT_URL can be used as an alternative for
# HORIZON_CONFIG.user_home, if user_home is not set.
# Do not set it to '/home/', as this will cause circular redirect loop
LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'static'))
STATIC_URL = '/static/'

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'HORIZON_CONFIG': HORIZON_CONFIG
}

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', ('lesscpy {infile}')),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'dashboard'
COMPRESS_CSS_HASHING_METHOD = 'hash'
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

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
    'kili',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = False
SESSION_TIMEOUT = 1800

# when doing upgrades, it may be wise to stick to PickleSerializer
# TODO(mrunge): remove after Icehouse
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LANGUAGES = (
    ('en', 'English'),
    ('en-au', 'Australian English'),
    ('en-gb', 'British English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ko', 'Korean (Korea)'),
    ('nl', 'Dutch (Netherlands)'),
    ('pl', 'Polish'),
    ('pt-br', 'Portuguese (Brazil)'),
    ('zh-cn', 'Simplified Chinese'),
)
LANGUAGE_CODE = 'en'
LANGUAGE_COOKIE_NAME = 'horizon_language'
USE_I18N = True
USE_L10N = True
USE_TZ = True

OPENSTACK_KEYSTONE_DEFAULT_ROLE = '_member_'

DEFAULT_EXCEPTION_REPORTER_FILTER = 'horizon.exceptions.HorizonReporterFilter'

POLICY_FILES_PATH = os.path.join(ROOT_PATH, "conf")
# Map of local copy of service policy files
POLICY_FILES = {
    'identity': 'keystone_policy.json',
    'compute': 'nova_policy.json',
    'volume': 'cinder_policy.json',
    'image': 'glance_policy.json',
    'orchestration': 'heat_policy.json',
}
LOCAL_PATH = None

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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'horizon.context_processors.horizon',
    'openstack_dashboard.context_processors.openstack',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader'
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
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

STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

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

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_dashboard': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'novaclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cinderclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'keystoneclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'glanceclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'neutronclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'heatclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ceilometerclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'troveclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'swiftclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'nose.plugins.manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}
