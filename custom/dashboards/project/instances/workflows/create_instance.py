from horizon import forms
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.project.instances.workflows.\
    create_instance import *


class CustomSetAccessControlsAction(SetAccessControlsAction):
    keypair = forms.DynamicChoiceField(label=_("Key Pair123"),
                                       required=True,
                                       help_text=_("Which key pair to use for "
                                                   "authentication."),
                                       add_item_link=KEYPAIR_IMPORT_URL)


class CustomSetAccessControls(SetAccessControls):
    action_class = CustomSetAccessControlsAction


class CustomLaunchInstance(LaunchInstance):
    default_steps = (SelectProjectUser,
                     SetInstanceDetails,
                     CustomSetAccessControls,
                     SetNetwork,
                     PostCreationStep,
                     SetAdvanced)
