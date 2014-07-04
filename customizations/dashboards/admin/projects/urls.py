from customizations.dashboards.admin.projects import views
from django.conf import urls

urlpatterns = [
    urls.url(r'^$', views.CustomIndexView.as_view(), name='index'),
    urls.url(r'^(?P<project_id>[^/]+)/promotion/$',
             views.GrantPromotionView.as_view(),
             name='promotion'),
    urls.url(r'^(?P<project_id>[^/]+)/transaction_history/$',
             views.TransactionHistoryView.as_view(),
             name='transaction_history')]
