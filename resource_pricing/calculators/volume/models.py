from django.db import models


class VolumeType(models.Model):
    os_type_id = models.CharField(primary_key=True, max_length=36)
    resource_id = models.IntegerField(db_index=True, unique=True)

    class Meta:
        db_table = "pricing_volume_type_resource"
