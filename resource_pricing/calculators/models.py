from django.db import models
from resource_pricing.models import ResourceBase


class InstanceType(ResourceBase):
    os_instance_type_id = models.CharField(max_length=36,
                                           unique=True,
                                           db_index=True)


class VolumeType(ResourceBase):
    os_volume_type_id = models.CharField(max_length=36,
                                         unique=True,
                                         db_index=True)
