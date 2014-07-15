from billing_app.payments import views
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa
from django.views.decorators.cache import cache_page  # noqa

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'cards/add$', views.AddCardView.as_view(), name='add_card'),
    url(r'cards/addfunds$', views.CardPayView.as_view(), name='add_funds'),
    url(r'mobilemoney/addnumber$',
        views.AddMobileNumberView.as_view(),
        name='add_number'),
    url(r'mobilemoney/transactioncode$',
        views.EnterTransactionCodeView.as_view(),
        name='enter_transaction_code'),
)
