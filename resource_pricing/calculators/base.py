from django.conf import settings
from django.core import exceptions
from resource_pricing import models
from resource_pricing import types


class CalculatorBase(object):
    types = types.ResourceTypes()
    type_name = "base"
    required_params = []
    optional_params = []

    def __init__(self):
        if not self._type_is_configured():
            raise Exception("the type {0} is not configured".format(
                self.type_name))

    def _type_is_configured(self):
        if self.type_name in settings.BILLABLE_RESOURCE_TYPES.keys():
            return True
        return False

    def _validate_params(self, params):
        checking = params.copy()
        for x in self.required_params:
            if x not in checking:
                raise Exception("the required parameter {0} is missing".
                                format(x))
            checking.pop(x)
        for x in checking.keys():
            if x not in self.optional_params:
                raise Exception("the given parameter {0} is unknown".
                                format(x))

    def _get_resource_price(self, resource_id, currency="USD"):
        try:
            price = models.Price.objects.get(currency__iso=currency,
                                             resource=resource_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find price for resource {0} with"
                            " currency {1}".format(resource_id, currency))
        return price.price
