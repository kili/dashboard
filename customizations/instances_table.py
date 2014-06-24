from customizations.dashboards.project.instances import views
from openstack_dashboard.dashboards.project import instances


class InstancesTableCustomizer:

    def execute(self):
        instances.views.IndexView.table_class = views.CustomInstancesTable
