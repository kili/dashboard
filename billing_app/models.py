from django.db import models
from billing_app.managers import StripeCustomerManager


class StripeCustomer(models.Model):

    name = models.CharField(max_length=64, unique=False, blank=False)
    is_default = models.BooleanField()
    keystone_id = models.CharField(max_length=64, unique=False, blank=False)
    stripe_customer_id = models.CharField(max_length=64, unique=True, blank=False)

    objects = StripeCustomerManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = (("name", "keystone_id"), ("is_default", "keystone_id"))
