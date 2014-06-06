from django.conf import settings


class ResourceTypes(object):
    brt = settings.BILLABLE_RESOURCE_TYPES

    def get_price_calculator(self, name):
        return self.brt[name]['price_calculator']
