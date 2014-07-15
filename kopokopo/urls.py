from django.conf.urls import patterns
from django.conf.urls import url
from kopokopo import views


urlpatterns = patterns('',
    url(r'^v2$',
        views.KopoKopoView.as_view(),
        name='kopokopo_api'))
