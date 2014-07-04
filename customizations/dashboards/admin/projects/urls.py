from django.conf import urls
from customizations.dashboards.admin.projects import views

urlpatterns = [
    urls.url(r'^$', views.CustomIndexView.as_view(), name='index'),
    urls.url(r'^(?P<project_id>[^/]+)/promotion/$',
             views.GrantPromotionView.as_view(),
             name='promotion')]
