from billing_app.payments import views
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'cards/add$', views.AddCardView.as_view(), name='add_card'),
    url(r'cards/addfunds$', views.CardPayView.as_view(), name='add_funds'),
)
