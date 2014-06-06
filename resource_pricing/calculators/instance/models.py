from django.db import models
from resource_pricing import models as resource_pricing_models


class Flavor(models.Model):
    os_flavor_id = models.CharField(primary_key=True, max_length=36)
    resource = models.ForeignKey(resource_pricing_models.Resource)

    class Meta:
        db_table = "pricing_instance_flavor_resource"
