from billing_app.usage import forms
from billing_app.usage import tables as usage_tables
from horizon import tables as horizon_tables
from resource_pricing import priced_usage
from user_billing.metering.ceilometer import data_fetcher


class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing_app/usage/index.html'
    table_classes = (usage_tables.InstanceUsageTable,)
    date_range_class = forms.DateRangeForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.date_range.form
        return context

    def get_instances_data(self):
        self.date_range = self.date_range_class(self.request)
        from_until_ts = self.date_range.get_date_range()
        stats = data_fetcher.CeilometerStats().get_stats(
            data_fetcher.StatsQuery(
                meter='instance',
                project_id=self.request.user.tenant_id,
                from_ts=from_until_ts[0],
                until_ts=from_until_ts[1]))
        return [usage_tables.InstanceUsageTableEntry(id=x['id'],
                                                     name=x['res_string'],
                                                     flavor=x['flavor'],
                                                     hours=x['hours'],
                                                     price=x['price'])
                for x in priced_usage.PricedUsageBase.get_meter_class(
                    'instance').get_priced_stats(stats)]
