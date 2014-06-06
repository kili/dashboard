from django.db import models


class Currency(models.Model):
    currency_iso = models.CharField(max_length=3)

    class Meta:
        db_table = "pricing_currency"


class ResourcePrice(models.Model):
    resource_id = models.IntegerField(primary_key=True)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        db_table = "pricing_resource_price"
