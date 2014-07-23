import billing
from billing_app import managers
from django.forms import ValidationError
from django.db import models
from django.db import IntegrityError
from django.db import DatabaseError
import logging

logger = logging.getLogger('horizon')


class Card(models.Model):

    last4 = models.CharField(max_length=64,
                             unique=False,
                             blank=False)
    tenant_id = models.CharField(max_length=64,
                                 unique=False,
                                 blank=False,
                                 db_index=True)
    stripe_customer_id = models.CharField(max_length=64,
                                          unique=True,
                                          blank=False)
    default = models.BooleanField(default=True)

    class Meta:
        unique_together = (("last4", "tenant_id"))

    def __unicode__(self):
        return u'{}'.format(self.name)

    @staticmethod
    def _get_stripe():
        return billing.get_gateway("stripe").stripe

    @property
    def name(self):
        return u'x{}'.format(self.last4)

    def save(self, *args, **kwargs):
        if not self.__class__.objects.filter(
                tenant_id=self.tenant_id,
                default=True).exists():
            self.default = True
        if self.default:
            self.__class__.objects.filter(
                tenant_id=self.tenant_id).update(default=False)
        super(Card, self).save(*args, **kwargs)

    def make_default(self):
        self.default = True
        self.save()

    @classmethod
    def create(cls, **kwargs):
        stripe = cls._get_stripe()
        try:
            # Create a Stripe Customer
            stripe_customer = stripe.Customer.create(
                card=kwargs['stripe_card_token'],
                description=kwargs['last4'],
                email=kwargs['email'])
        except stripe.error.CardError as e:
            logger.error('Card is not valid')
            raise ValidationError(e.message)
        except (stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
            logger.error('Could not create stripe customer: %s', e.message)
            raise IntegrityError('Error creating customer on Stripe backend, '
                                 'please contact support')
        card = cls(last4=kwargs['last4'],
                   default=kwargs['default'],
                   tenant_id=kwargs['tenant_id'],
                   stripe_customer_id=stripe_customer.id)
        try:
            card.save()
        except (IntegrityError, DatabaseError):
            stripe_customer.delete()
            logger.exception('error, couldnt insert into db')
            raise IntegrityError('Error creating card in db')
        return card

    def delete(self, *args, **kwargs):
        try:
            self._get_stripe().Customer.retrieve(
                self.stripe_customer_id).delete()
        except Exception:
            logger.error('Could not delete card: %s', self.stripe_customer_id)
        finally:
            super(Card, self).delete(*args, **kwargs)


class MobileMoneyNumber(models.Model):

    number = models.CharField(max_length=64,
                              unique=True,
                              blank=False)
    tenant_id = models.CharField(max_length=64,
                                 unique=False,
                                 blank=False)

    objects = managers.MobileMoneyNumberManager()

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def create(cls, **kwargs):
        number = cls(**kwargs)
        number.save()
        return number


class KopoKopoTransaction(models.Model):
    service_name = models.CharField(max_length=64, blank=True)
    business_number = models.CharField(max_length=64, blank=True)
    transaction_reference = models.CharField(
        max_length=64, blank=True, unique=True)
    internal_transaction_id = models.CharField(
        max_length=64, blank=True, unique=True)
    transaction_timestamp = models.DateTimeField(blank=True)
    transaction_type = models.CharField(max_length=64, blank=True)
    account_number = models.CharField(max_length=64, blank=True)
    sender_phone = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    middle_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=64)
    signature = models.CharField(max_length=64)
    claimed = models.BooleanField(default=False)


class PrePaidReservation(models.Model):
    instance_type = models.CharField(max_length=64)
    hourly_price = models.DecimalField(max_digits=19, decimal_places=10)
    total_price = models.DecimalField(max_digits=19, decimal_places=10)
    length = models.PositiveSmallIntegerField()
    available = models.BooleanField(default=False)


class AssignedReservation(models.Model):
    tenant_id = models.CharField(max_length=64,
                                 blank=False)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    prepaid_reservation = models.ForeignKey('PrePaidReservation')
