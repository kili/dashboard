from django.conf.urls import patterns, include, url
import openstack_dashboard

urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^$', 'kili.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('openstack_dashboard.urls')),
)
