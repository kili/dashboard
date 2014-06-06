from django.conf import settings


class ResourceTypes(object):
    brt = settings.BILLABLE_RESOURCE_TYPES

    def get_price_calculator(self, name):
        try:
            return self.brt[name]['price_calculator']
        except KeyError:
            raise Exception(
                'the price calculator for type {0} is not configured'.format(
                    name))
