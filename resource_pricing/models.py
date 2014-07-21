from django.db import models


class Currency(models.Model):
    iso = models.CharField(max_length=3, db_index=True)


# base resource for type specific resource info
# in resource_pricing.calculators.models
class ResourceBase(models.Model):
    pass


class Price(models.Model):
    currency = models.ForeignKey(Currency)
    resource = models.ForeignKey(ResourceBase)
    price = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        unique_together = ('currency', 'resource')
