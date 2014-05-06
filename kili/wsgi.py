"""
WSGI config for kili project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from django.conf import settings
import django.core.handlers.wsgi
import newrelic.agent
import os
import sys

# Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'kili.local.local_settings'
sys.stdout = sys.stderr

DEBUG = False

application = django.core.handlers.wsgi.WSGIHandler()

if settings.ENV_NAME == "prod":
    newrelic.agent.initialize(settings.NEWRELIC_CONFIG_FILE, settings.ENV_NAME)
    application = newrelic.agent.wsgi_application()(application)
