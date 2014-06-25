from accounting import managers
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.project.instances.tables import *  # noqa


class CustomLaunchLink(LaunchLink):
    name = "launch"
    sufficient_money = True
    verbose_name = _("Launch Instance")
    url = "horizon:project:instances:launch"
    classes = ("btn-launch", "ajax-modal")
    policy_rules = (("compute", "compute:create"),)

    def allowed(self, request, datum):
        self.account_manager = managers.AccountManager()
        self.sufficient_money = self.account_manager.has_sufficient_balance(
            self.table.request.user.tenant_id)
        if self.sufficient_money:
            self.classes = ('btn-launch', 'ajax-modal')
        else:
            self.classes = ('btn-launch')
        return super(CustomLaunchLink, self).allowed(request, datum)

    def get_link_url(self, datum=None):
        if not self.sufficient_money:
            return urlresolvers.reverse('horizon:billing:payments:index')
        return super(CustomLaunchLink, self).get_link_url(datum)


class CustomInstancesTable(InstancesTable):
    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        status_columns = ["status", "task"]
        row_class = UpdateRow
        table_actions = (CustomLaunchLink, SoftRebootInstance,
                         TerminateInstance, InstancesFilterAction)
        row_actions = (StartInstance, ConfirmResize, RevertResize,
                       CreateSnapshot, SimpleAssociateIP, AssociateIP,
                       SimpleDisassociateIP, EditInstance,
                       DecryptInstancePassword, EditInstanceSecurityGroups,
                       ConsoleLink, LogLink, TogglePause, ToggleSuspend,
                       ResizeLink, SoftRebootInstance, RebootInstance,
                       StopInstance, RebuildInstance, TerminateInstance)
