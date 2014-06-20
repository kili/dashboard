from django.db import models
from resource_pricing import models as resource_pricing_models


class Flavor(models.Model):
    id = models.AutoField(primary_key=True)
    os_flavor_id = models.CharField(max_length=36, unique=True, db_index=True)
    resource = models.ForeignKey(resource_pricing_models.Resource, unique=True, db_index=True)

    class Meta:
        db_table = "pricing_instance_flavor_resource"
