from openstack_dashboard.dashboards.project.instances.views \
    import LaunchInstanceView
from openstack_dashboard.dashboards.project.instances.workflows. \
    create_instance import *
from custom.dashboards.project.instances.workflows.create_instance import *


# replace SetAccessControls with CustomSetAccessControls
# to make a keypair selection required
LaunchInstanceView.workflow_class.default_steps = (SelectProjectUser,
                                                   SetInstanceDetails,
                                                   CustomSetAccessControls,
                                                   SetNetwork,
                                                   PostCreationStep,
                                                   SetAdvanced)
