from billing import get_integration
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa
from .views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'offsite/stripe/$', offsite_stripe', name='app_offsite_stripe'),
)
