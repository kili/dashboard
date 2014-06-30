from customizations.dashboards.project.instances import tables
from openstack_dashboard.dashboards.project import instances


class InstancesTableCustomizer:

    def execute(self):
        instances.views.IndexView.table_class = tables.CustomInstancesTable
