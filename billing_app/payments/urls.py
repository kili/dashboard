from billing_app.payments import views
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'offsite/stripe/$', offsite_stripe', name='app_offsite_stripe'),
)
