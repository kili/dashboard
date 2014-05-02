from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.project.instances.workflows.\
    create_instance import *


class CustomSetAccessControlsAction(SetAccessControlsAction):
    keypair = forms.DynamicChoiceField(label=_("Key Pair123"),
                                       required=True,
                                       help_text=_("Which key pair to use for "
                                                   "authentication."),
                                       add_item_link=KEYPAIR_IMPORT_URL)

    def __init__(self, request, *args, **kwargs):
        super(CustomSetAccessControlsAction, self).__init__(request, *args, **kwargs)
        if not api.nova.can_set_server_password():
            del self.fields['admin_pass']
            del self.fields['confirm_admin_pass']


class CustomSetAccessControls(SetAccessControls):
    action_class = CustomSetAccessControlsAction


class CustomLaunchInstance(LaunchInstance):
    default_steps = (SelectProjectUser,
                     SetInstanceDetails,
                     CustomSetAccessControls,
                     SetNetwork,
                     PostCreationStep,
                     SetAdvanced)
