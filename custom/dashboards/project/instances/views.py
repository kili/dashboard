from openstack_dashboard.dashboards.project.instances.views \
    import LaunchInstanceView
from custom.dashboards.project.instances \
    import workflows as project_workflows


class CustomLaunchInstanceView(LaunchInstanceView):
    workflow_class = project_workflows.CustomLaunchInstance
