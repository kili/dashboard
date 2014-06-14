from billing_app.usage import forms
from billing_app.usage import tables as usage_tables
from horizon import tables as horizon_tables
from resource_pricing import managers


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/usage/index.html'
    table_class = usage_tables.InstanceUsageTable
    date_range_class = forms.DateRangeForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.date_range.form
        return context

    def get_data(self):
        project_id = self.kwargs.get('project_id', self.request.user.tenant_id)
        self.date_range = self.date_range_class(self.request)
        return [usage_tables.InstanceUsageTableEntry(id=x['id'],
                                                     name=x['name'],
                                                     flavor=x['flavor'],
                                                     hours=x['hours'],
                                                     price=x['price'])
                for x in managers.PricedInstanceUsage.get_overview(
                    project_id, self.date_range.get_date_range())]
