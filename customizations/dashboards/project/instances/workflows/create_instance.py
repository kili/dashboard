from accounting import managers
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from openstack_dashboard import api
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


class CustomSetInstanceDetailsAction(create_instance.SetInstanceDetailsAction):
    availability_zone = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        name = _("Details")
        help_text_template = ("project/instances/"
                              "_launch_details_help.html")

    def __init__(self, request, *args, **kwargs):
        super(CustomSetInstanceDetailsAction, self).__init__(
            request, *args, **kwargs)
        try:
            zones = api.nova.availability_zone_list(request)
        except Exception:
            zones = []
            exceptions.handle(request,
                              'Unable to retrieve availability zones.')
        self.fields['availability_zone'].initial = [
            zone.zoneName
            for zone in zones if zone.zoneState['available']][0]


class CustomSetAccessControls(create_instance.SetAccessControls):
    action_class = CustomSetAccessControlsAction


class CustomSetInstanceDetails(create_instance.SetInstanceDetails):
    action_class = CustomSetInstanceDetailsAction


class CustomLaunchInstance(create_instance.LaunchInstance):
    default_steps = (create_instance.SelectProjectUser,
                     # customized instance details tab
                     CustomSetInstanceDetails,
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
            raise exceptions.Http302(urlresolvers.reverse(
                'horizon:billing:payments:index'))
        return super(CustomLaunchInstanceView, self).dispatch(*args, **kwargs)
