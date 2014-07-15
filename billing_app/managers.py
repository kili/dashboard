import billing
from django.core.exceptions import ObjectDoesNotExist  # noqa
from django.db import (models, IntegrityError)  # noqa
from django.utils.translation import ugettext_lazy as _


class StripeCustomerManager(models.Manager):

    def delete_card(self, id, tenant_id):
        stripe = billing.get_gateway("stripe").stripe
        try:
            card = self.get(
                id__exact=id,
                tenant_id__exact=tenant_id
            )
            stripe_cust = stripe.Customer.retrieve(card.stripe_customer_id)
            stripe_cust.delete()
            card.delete()
            return (True,)
        except stripe.error.StripeError as e:
            # Display a very generic error to the user
            if e.http_status == 404:
                card.delete()
                return (True,)
            return (False, e.message)
        except ObjectDoesNotExist as e:
            return (False, u'Card does not exist')
        except Exception:
            return (False, _("Could not delete card. "
                             "Please try again later"))


class MobileMoneyNumberManager(models.Manager):

    def add_number(self, number, tenant_id):
        mobilenumber = self.model(number=number, tenant_id=tenant_id)

        try:
            mobilenumber.save()
        except IntegrityError:
            return (False, _("That number %s isn't available"
                             "for use") % mobilenumber.number)
        except Exception:
            return (False, _("Could not add number. Try again later."))

        return (True,)

    def delete_number(self, id, tenant_id):
        try:
            mobilenumber = self.get(
                id__exact=id,
                tenant_id__exact=tenant_id
            )
            mobilenumber.delete()
            return (True,)
        except IntegrityError:
            return (False, _("That number %s isn't available"
                             "for use") % mobilenumber.number)
        except Exception:
            return (False, _("Could not delete Number. "
                             "Please try again later"))
        return (True,)
