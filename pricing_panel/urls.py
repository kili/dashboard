from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from pricing_panel import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<resource_price_id>[^/]+)/update/$',
        views.UpdateView.as_view(), name='update'),
)
