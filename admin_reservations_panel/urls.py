from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa
from admin_reservations_panel import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'create$', views.CreateReservationView.as_view(), name='create'),
)
