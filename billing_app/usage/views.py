from billing_app.usage import forms
from billing_app.usage import tables as usage_tables
from horizon import tables as horizon_tables
from resource_pricing import priced_usage
from project_billing.ceilometer_fetcher import CeilometerStats


class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing/usage/index.html'
    table_classes = (usage_tables.InstanceUsageTable,)
    date_range_class = forms.DateRangeForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.date_range.form
        return context

    def get_instances_data(self):
        self.date_range = self.date_range_class(self.request)
        from_until_ts = self.date_range.get_date_range()
        return [usage_tables.InstanceUsageTableEntry(id=stats['id'],
                                                     name=stats['res_string'],
                                                     flavor=stats['flavor'],
                                                     hours=stats['hours'],
                                                     price=stats['price'])
                for stats in priced_usage.PricedUsageBase.get_meter_class(
                    'instance').get_priced_stats(
                        CeilometerStats.get_stats(
                            meter='instance',
                            project_id=self.request.user.tenant_id,
                            from_ts=from_until_ts[0],
                            until_ts=from_until_ts[1]))]
