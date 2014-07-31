from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from billing_app.reservations import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<id>[^/]+)/purchase$',
        views.PurchaseView.as_view(), name='purchase'),
)
