from django.conf import settings
from django.conf import urls


urlpatterns = urls.patterns('',
    urls.url(r'^kopokopo/', urls.include('kopokopo.urls')),
    urls.url(r'^accounts/', urls.include('allauth.urls')),
    urls.url(r'', urls.include('openstack_dashboard.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += urls.patterns('',
        urls.url(r'^__debug__/', urls.include(debug_toolbar.urls)),
    )
