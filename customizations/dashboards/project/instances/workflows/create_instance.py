from accounting import managers
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from openstack_dashboard.dashboards.project.instances import views
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


class CustomSetAccessControls(create_instance.SetAccessControls):
    action_class = CustomSetAccessControlsAction


class CustomLaunchInstance(create_instance.LaunchInstance):
    default_steps = (create_instance.SelectProjectUser,
                     create_instance.SetInstanceDetails,
                     # customized access control tab
                     CustomSetAccessControls,
                     create_instance.SetNetwork,
                     create_instance.PostCreationStep,
                     create_instance.SetAdvanced)


class CustomLaunchInstanceView(views.LaunchInstanceView):
    workflow_class = CustomLaunchInstance

    def __init__(self, *args, **kwargs):
        super(CustomLaunchInstanceView, self).__init__(*args, **kwargs)
        self.account_manager = managers.AccountManager()

    def dispatch(self, *args, **kwargs):
        if not self.account_manager.has_sufficient_balance(
                self.request.user.tenant_id):
            raise exceptions.Http302('/billing/')
        return super(CustomLaunchInstanceView, self).dispatch(*args, **kwargs)
