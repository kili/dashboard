from billing_app.payments import views
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

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
    url(r'mobilemoney/K2/v2$',
        views.K2_v2.as_view(),
        name='k2_ver2_endpoint'),
)
