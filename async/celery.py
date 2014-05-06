from __future__ import absolute_import
import celery
from django.conf import settings


celery_app = celery.Celery('async', include=['async.tasks'])
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
