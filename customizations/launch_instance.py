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
        LaunchInstanceView.workflow_class.default_steps = self.get_default_steps()

    def get_default_steps(self):
        return (SelectProjectUser,
                SetInstanceDetails,
                # customized access control tab
                CustomSetAccessControls,
                SetNetwork,
                PostCreationStep,
                SetAdvanced)
