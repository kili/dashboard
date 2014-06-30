from accounting import managers
from customizations.dashboards.admin.users import tables
from openstack_dashboard.dashboards.admin.users import views


class CustomIndexView(views.IndexView):
    table_class = tables.CustomUsersTable

    def get_data(self, *args, **kwargs):
        am = managers.AccountManager()
        data = super(CustomIndexView, self).get_data(*args, **kwargs)
        for obj in data:
            setattr(obj,
                    'balance',
                    am.get_user_account(obj.tenantId).balance())
        return data
