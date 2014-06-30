from customizations.dashboards.admin.users import views
from django.conf import urls
from openstack_dashboard.dashboards.admin.users import urls as user_urls


class UserTableCustomizer:

    def execute(self):
        user_urls.urlpatterns.insert(0, urls.url(
            r'^$', views.CustomIndexView.as_view(), name='index'))
