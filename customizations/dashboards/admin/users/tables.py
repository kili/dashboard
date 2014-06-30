from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.admin.users.tables import *  # noqa
from user_billing import helpers


class CustomUsersTable(UsersTable):
    balance = tables.Column('balance',
                            filters=[helpers.FormattingHelpers.price],
                            verbose_name='Balance')

    class Meta:
        name = "users"
        verbose_name = _("Users")
        row_actions = (EditUserLink, ToggleEnabled, DeleteUsersAction)
        table_actions = (UserFilterAction, CreateUserLink, DeleteUsersAction)
