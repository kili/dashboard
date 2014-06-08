from django.db import models


class Currency(models.Model):
    currency_iso = models.CharField(max_length=3)


class Resource(models.Model):
    counter_name = models.CharField(max_length=30)


class Price(models.Model):
    resource = models.ForeignKey(Resource)
    currency = models.ForeignKey(Currency)
    price = models.IntegerField()

    class Meta:
        unique_together = ("resource", "currency")
