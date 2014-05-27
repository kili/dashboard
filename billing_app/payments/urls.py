from billing import get_integration
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from .views import IndexView
stripe_obj = get_integration("stripe_example")

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'offsite/stripe/$', offsite_stripe', name='app_offsite_stripe'),
    url(r'^stripe/', include(stripe_obj.urls)),
)
