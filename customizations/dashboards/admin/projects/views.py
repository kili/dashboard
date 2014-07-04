from accounting import transactions
from accounting import managers
from billing_app.history import tables as billing_hist_tables
from customizations.dashboards.admin.projects import tables as project_tables
from customizations.dashboards.admin.projects import forms as project_forms
from django.core import urlresolvers
from horizon import forms
from horizon import tables
from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.projects import views


class CustomIndexView(views.IndexView):
    table_class = project_tables.CustomTenantsTable

    def get_data(self, *args, **kwargs):
        am = managers.AccountManager()
        data = super(CustomIndexView, self).get_data(*args, **kwargs)
        for obj in data:
            setattr(obj,
                    'balance',
                    am.get_user_account(obj.id).balance())
        return data


class GrantPromotionView(forms.ModalFormView):
    form_class = project_forms.GrantPromotionForm
    template_name = 'admin/projects/promotion.html'
    success_url = urlresolvers.reverse_lazy('horizon:admin:projects:index')

    def get_context_data(self, **kwargs):
        return dict(
            super(GrantPromotionView, self).get_context_data(**kwargs).items() +
                  [('promotion', {'project_id': self.kwargs['project_id']})])

    def get_initial(self):
        return {'project_id': self.kwargs['project_id']}


class TransactionHistoryView(tables.DataTableView):
    template_name = 'billing_app/history/index.html'
    table_class = billing_hist_tables.TransactionHistoryTable

    def get_context_data(self, **kwargs):
        context = super(TransactionHistoryView, self).get_context_data(**kwargs)
        context['project'] = api.keystone.tenant_get(self.request, context['project_id']).name
        return context

    def get_data(self):
        return [billing_hist_tables.TransactionHistoryTableEntry(
            x['tid'],
            x['timestamp'],
            x['description'],
            x['amount']) for x in transactions.TransactionHistory().
            get_user_account_transaction_history(
                self.kwargs['project_id'], user_values=True)]
