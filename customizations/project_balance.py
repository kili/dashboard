from customizations.dashboards.admin.projects import urls as custom_urls
from openstack_dashboard.dashboards.admin.projects import urls as project_urls


class ProjectTableCustomizer:

    def execute(self):
        project_urls.urlpatterns = (custom_urls.urlpatterns +
                                    project_urls.urlpatterns)
