from billing_app.managers import k2_raw_data_manager
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
    tenant_id = models.CharField(max_length=64,
                                 unique=False,
                                 blank=False)

    objects = MobileMoneyNumberManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = (("number", "tenant_id"))


class k2_raw_data(models.Model):
    service_name = models.CharField(max_length=64)
    business_number = models.CharField(max_length=64, blank=False)
    transaction_reference = models.CharField(max_length=64, blank=False)
    internal_transaction_id = models.CharField(max_length=64)
    transaction_timestamp = models.DateTimeField(blank=False)
    transaction_type = models.CharField(max_length=64)
    account_number = models.CharField(max_length=64)
    sender_phone = models.CharField(max_length=64, blank=False)
    first_name = models.CharField(max_length=64, blank=False)
    middle_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    amount = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=64, blank=False)
    signature = models.CharField(max_length=64, blank=False)

    objects = k2_raw_data_manager()
