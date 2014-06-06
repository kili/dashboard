from django.conf import settings


class ResourceTypes(object):
    brt = settings.BILLABLE_RESOURCE_TYPES

    def get_id_by_name(self, name):
        return self.brt[name]['id']

    def get_name_by_id(self, id):
        name = [x for x in self.brt.keys() if self.brt[x]['id'] == id]
        if name == []:
            raise KeyError(id)
        return name

    def get_price_calculator_by_name(self, name):
        return self.brt[name]['price_calculator']
