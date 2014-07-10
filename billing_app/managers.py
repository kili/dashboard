import billing
from django.db import (models, IntegrityError)  # noqa
from django.utils.translation import ugettext_lazy as _


class StripeCustomerManager(models.Manager):

    def delete_card(self, id, keystone_id):
        stripe = billing.get_gateway("stripe").stripe
        try:
            card = self.get(
                id__exact=id,
                keystone_id__exact=keystone_id
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
        except Exception:
            return (False, _("Could not delete card. "
                             "Please try again later"))


class MobileMoneyNumberManager(models.Manager):

    def add_number(self, number, keystone_id):
        mobilenumber = self.model(number=number, keystone_id=keystone_id)

        try:
            mobilenumber.save()
        except IntegrityError:
            return (False, _("That number %s isn't available"
                             "for use") % mobilenumber.number)
        except Exception:
            return (False, _("Could not add number. Try again later."))

        return (True,)

    def delete_number(self, id, keystone_id):
        try:
            mobilenumber = self.get(
                id__exact=id,
                keystone_id__exact=keystone_id
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
