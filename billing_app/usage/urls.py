from billing_app.usage import views
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),  # noqa
)
