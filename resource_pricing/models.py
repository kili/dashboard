from django.db import models
from user_billing import helpers


class Currency(models.Model):
    iso = models.CharField(max_length=3, db_index=True)

    def __unicode__(self):
        return u'{0}'.format(self.iso)

    class Meta:
        db_table = "pricing_currency"


class Resource(models.Model):
    description = models.CharField(max_length=100, db_index=True)
    resource_type_id = models.IntegerField()

    def __unicode__(self):
        return u'{0}'.format(self.description)

    class Meta:
        db_table = "pricing_resource"


class Price(models.Model):
    currency = models.ForeignKey(Currency)
    resource = models.ForeignKey(Resource)
    price = models.DecimalField(max_digits=19, decimal_places=10)

    def __unicode__(self):
        return u'price {0} for {1} in {2}'.format(
            helpers.FormattingHelpers.price(self.price),
            self.resource.description,
            self.currency.iso)

    class Meta:
        db_table = "pricing_resource_currency_price"
        unique_together = ('currency', 'resource')
