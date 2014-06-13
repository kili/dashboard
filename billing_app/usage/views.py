from billing_app.usage import tables as usage_tables
from horizon import tables as horizon_tables
from openstack_dashboard import usage
from resource_pricing import managers


class ResourceUsage(usage.BaseUsage):
    attrs = ('resource', 'hours', 'price')

    def summarize(self, *args, **kwargs):
        return managers.PricedUsageManager.get_overview(self.project_id,
                                                        args)


class UsageTableEntry():

    def __init__(self, id, resource, hours, price):
        self.id = id
        self.resource = resource
        self.hours = hours
        self.price = price


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/usage/index.html'
    table_class = usage_tables.UsageTable
    usage_class = ResourceUsage

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.usage.form
        return context

    def get_data(self):
        project_id = self.kwargs.get('project_id', self.request.user.tenant_id)
        self.usage = self.usage_class(self.request, project_id)
        return [UsageTableEntry(x['id'], x['resource'], x['hours'], x['price'])
                for x in self.usage.summarize(*self.usage.get_date_range())]
