from billing_app.managers import MobileMoneyNumberManager
from billing_app.managers import StripeCustomerManager
from django.db import models


class StripeCustomer(models.Model):

    name = models.CharField(max_length=64,
                            unique=False,
                            blank=False)
    is_default = models.BooleanField()
    keystone_id = models.CharField(max_length=64,
                                   unique=False,
                                   blank=False)
    stripe_customer_id = models.CharField(max_length=64,
                                          unique=True,
                                          blank=False)

    objects = StripeCustomerManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = (("name", "keystone_id"))

class MobileMoneyNumber(models.Model):

    number = models.CharField(max_length=64,
                            unique=False,
                            blank=False)
    keystone_id = models.CharField(max_length=64,
                                   unique=False,
                                   blank=False)

    objects = MobileMoneyNumberManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = (("number", "keystone_id"))
