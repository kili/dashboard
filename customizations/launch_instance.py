from openstack_dashboard.dashboards.project.instances.views \
    import LaunchInstanceView
from openstack_dashboard.dashboards.project.instances.workflows. \
    create_instance import *
from customizations.dashboards.project.instances.workflows.create_instance \
    import *


class LaunchInstanceViewCustomizer:

    def execute(self):
        """
        replace SetAccessControls with CustomSetAccessControls
        to make a keypair selection required
        """
        LaunchInstanceView.workflow_class.default_steps = (
            SelectProjectUser,
            SetInstanceDetails,
            CustomSetAccessControls,
            SetNetwork,
            PostCreationStep,
            SetAdvanced)
