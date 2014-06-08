from django.db import models


class Currency(models.Model):
    iso = models.CharField(max_length=3, db_index=True)

    class Meta:
        db_table = "pricing_currency"


class Resource(models.Model):
    description = models.CharField(max_length=100, db_index=True)
    resource_type_id = models.IntegerField()

    class Meta:
        db_table = "pricing_resource"


class Price(models.Model):
    currency = models.ForeignKey(Currency)
    resource = models.ForeignKey(Resource)
    price = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        db_table = "pricing_resource_currency_price"
        unique_together = ('currency', 'resource')
