from django.utils.translation import ugettext_lazy as _
from horizon import forms
from openstack_dashboard.dashboards.project.instances.workflows \
    import create_instance

KEYPAIR_IMPORT_URL = "horizon:project:access_and_security:keypairs:import"


class CustomSetAccessControlsAction(create_instance.SetAccessControlsAction):
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


class CustomSetAccessControls(create_instance.SetAccessControls):
    action_class = CustomSetAccessControlsAction

    def __init__(self, *args, **kwargs):
        super(CustomSetAccessControls, self).__init__(*args, **kwargs)
