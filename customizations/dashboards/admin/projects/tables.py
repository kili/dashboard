from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.admin.projects.tables import *  # noqa
from project_billing import helpers


class ProjectPromotionLink(tables.LinkAction):
    name = "promotion"
    verbose_name = _("Grant Promotion")
    url = "horizon:admin:projects:promotion"
    classes = ("ajax-modal", "btn-promotion")
    policy_rules = (("identity", "identity:update_project"),
                    ("identity", "identity:list_projects"),)

    def allowed(self, request, user):
        return request.user.is_superuser


class TransactionHistoryLink(tables.LinkAction):
    name = "transaction history"
    verbose_name = _("Transaction History")
    url = "horizon:admin:projects:transaction_history"
    classes = ("btn-transhist")
    policy_rules = (("identity", "identity:update_project"),
                    ("identity", "identity:list_projects"),)

    def allowed(self, request, user):
        return request.user.is_superuser


class CustomTenantsTable(TenantsTable):
    balance = tables.Column('balance',
                            filters=[helpers.FormattingHelpers.price],
                            verbose_name='Balance')

    class Meta:
        name = "tenants"
        verbose_name = _("Projects")
        row_class = UpdateRow
        row_actions = (ViewMembersLink, ViewGroupsLink, UpdateProject,
                       UsageLink, ModifyQuotas, DeleteTenantsAction,
                       ProjectPromotionLink, TransactionHistoryLink)
        table_actions = (TenantFilterAction, CreateProject,
                         DeleteTenantsAction)
        pagination_param = "tenant_marker"
