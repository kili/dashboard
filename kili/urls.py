from django.conf.urls import patterns, include, url
from django.conf import settings
import openstack_dashboard


urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('openstack_dashboard.urls')),
    url(r'', include('custom.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
