from horizon import forms
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.project.instances.workflows.\
    create_instance import *


class CustomSetAccessControlsAction(SetAccessControlsAction):
    keypair = forms.DynamicChoiceField(label=_("Key Pair"),
                                       required=True,
                                       help_text=_("Which key pair to use for "
                                                   "authentication."),
                                       add_item_link=KEYPAIR_IMPORT_URL)

    class Meta:
        name = _("Access & Security")
        help_text = _("Control access to your instance via key pairs, "
                      "security groups, and other mechanisms.")

    def __init__(self, *args, **kwargs):
        super(CustomSetAccessControlsAction, self).__init__(*args, **kwargs)


class CustomSetAccessControls(SetAccessControls):
    action_class = CustomSetAccessControlsAction

    def __init__(self, *args, **kwargs):
        super(CustomSetAccessControls, self).__init__(*args, **kwargs)