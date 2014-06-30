import billing
from django.db import (models, IntegrityError)  # noqa
from django.utils.translation import ugettext_lazy as _


class StripeCustomerManager(models.Manager):

    def create_stripe_customer(self, name, is_default,
                               keystone_id, stripe_customer_id):
        card = self.model(name=name,
                          is_default=is_default,
                          keystone_id=keystone_id,
                          stripe_customer_id=stripe_customer_id)

        # make the card default there's no other
        if not self.all():
            card.is_default = True
        try:
            card.save()
        except IntegrityError:
            return (False, _("You already have a card"
                             " by the number :- %s") % card.name)
        except Exception:
            return (False, _("Could not add card. Try again later."))

        if card.is_default:
            return self.ensure_default(card.id, keystone_id)

        return (True,)

    def ensure_default(self, id, keystone_id):
        try:
            old_defaults = self.filter(keystone_id__exact=keystone_id,
                                       is_default=True).exclude(id__exact=id)
            for card in old_defaults:
                card.is_default = False
                card.save()

            new_default = self.get(id__exact=id,
                                   keystone_id__exact=keystone_id)

            new_default.is_default = True
            new_default.save()
            return (True,)
        except Exception:
            return (False, _("Card added but not as default."))

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


class k2_raw_data_manager(models.Manager):

    def create(self, k2data):
        k2_entry = self.model(
            service_name=k2data['service_name'],
            business_number=k2data['business_number'],
            transaction_reference=k2data['transaction_reference'],
            internal_transaction_id=k2data['internal_transaction_id'],
            transaction_timestamp=k2data['transaction_timestamp'],
            transaction_type=k2data['transaction_type'],
            account_number=k2data['account_number'],
            sender_phone=k2data['sender_phone'],
            first_name=k2data['first_name'],
            middle_name=k2data['middle_name'],
            last_name=k2data['last_name'],
            amount=k2data['amount'],
            currency=k2data['currency'],
            signature=k2data['signature'])
        k2_entry.save()
