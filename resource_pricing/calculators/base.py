from resource_pricing import types


class CalculatorBase(object):
    types = types.ResourceTypes()
    type_name = 'base'
    required_params = []
    optional_params = []

    def _type_is_configured(self):
        try:
            self.types.get_id_by_name(self.type_name)
        except KeyError:
            return False
        return True

    def _validate_params(self, params):
        checking = params.copy()
        for x in self.required_params:
            if not checking.has_key(x):
                raise Exception("the required parameter {0} is missing".
                                format(x))
            checking.pop(x)
        for x in checking.keys():
            if x not in self.optional_params:
                raise Exception("the given parameter {0} is unknown".
                                format(x))

    def get_unit_price(self, resource_type, params=None):
        raise NotImplementedError
