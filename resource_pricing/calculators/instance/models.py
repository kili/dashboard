from django.db import models


class Flavor(models.Model):
    os_flavor_id = models.CharField(primary_key=True, max_length=36)
    resource_id = models.IntegerField(db_index=True, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = "pricing_instance_flavor_resource"
