from billing_app.usage import tables as usage_tables
from horizon import tables as horizon_tables
from resource_pricing import managers


class UsageTableEntry():

    def __init__(self, id, resource, hours, price):
        self.id = id
        self.resource = resource
        self.hours = hours
        self.price = price


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/usage/index.html'
    table_class = usage_tables.UsageTable

    def get_data(self):
        return [UsageTableEntry(x['id'], x['resource'], x['hours'], x['price'])
                for x in managers.PricedUsageManager.get_overview(
                    '291ee2b894884bf0ad3754de434ae690')]
