from __future__ import absolute_import
from celery import Celery
from openstack_dashboard import settings


celery_app = Celery('async', include=['async.tasks'])
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
