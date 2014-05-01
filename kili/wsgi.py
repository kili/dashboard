"""
WSGI config for kili project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import django.core.handlers.wsgi
from django.conf import settings
import newrelic.agent

# Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'kili.local.local_settings'
sys.stdout = sys.stderr

DEBUG = False

newrelic.agent.initialize(settings.NEWRELIC_CONFIG_FILE, settings.ENV_NAME)

application = django.core.handlers.wsgi.WSGIHandler()
application = newrelic.agent.wsgi_application()(application)
