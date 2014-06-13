from accounting import transactions
import billing
from billing.forms import stripe_forms  # noqa
from billing_app.models import StripeCustomer
import decimal
from django.forms import ValidationError  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from horizon import messages


stripe = billing.get_gateway("stripe").stripe


class AddCardForm(stripe_forms.StripeForm, forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        self.fields.pop('amount')

    card_name = forms.CharField(widget=forms.HiddenInput())
    make_default = forms.BooleanField(
        label=_("Make this my Default Card"),
        required=False
    )
    stripe_card_token = forms.CharField(widget=forms.HiddenInput())

    def handle(self, request, data):
        try:
            # Create a Stripe Customer
            stripe_customer = stripe.Customer.create(
                card=data['stripe_card_token'],
                description=data['card_name'],
                email=request.user.username
            )

            result = StripeCustomer.objects.create_stripe_customer(
                data['card_name'],
                data['make_default'],
                request.user.id,
                stripe_customer.id
            )
            if not result[0]:
                stripe_customer.delete()
                raise ValidationError(result[1])

            messages.success(
                request,
                _('Credit card "%s" has been tied to your account.')
                % data['card_name']
            )
            return True
        except stripe.error.CardError as e:
            # Card declined
            self.api_error(e.message)
            return False
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            self.api_error(e.message)
            return False
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            self.api_error(e.message)
            return False
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            self.api_error(e.message)
            return False
        except stripe.error.StripeError as e:
            # Display a very generic error to the user
            self.api_error(e.message)
            return False
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("Unknown error occured")
            return False


class CardPayForm(forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(CardPayForm, self).__init__(*args, **kwargs)

    amount = forms.DecimalField(label=_("Amount (In US Dollars)"),
                                required=True,
                                min_value=decimal.Decimal('15'))

    def handle(self, request, data):
        try:
            # Charge our Stripe Customer
            customerQS = StripeCustomer.objects.filter(
                keystone_id__exact=request.user.id,
                is_default=True
            )
            if not customerQS:
                raise ValidationError(_("Could not find default billing card. "
                                        "Please select one of your cards as "
                                        "the default for billing."))
            if data['amount'] < 15:
                raise ValidationError(_("Minimum payable amount is 15 USD. "))

            # register charge on stripe
            stripe.Charge.create(
                amount=data['amount'] * 100,  # stripe expects amount in cents.
                currency="usd",
                customer=customerQS.all()[0].stripe_customer_id
            )

            # credit user account
            ut = transactions.UserTransactions()
            ut.receive_user_payment(request.user.id, "STRIPE", data['amount'],
                                    "Received payment via Credit/Debit card")

            # profit!!!!
            messages.success(
                request,
                _('You have transferred %s USD to your account.')
                % data['amount']
            )
            return True
        except stripe.error.CardError as e:
            # Card declined
            self.api_error(e.message)
            return False
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            self.api_error(e.message)
            return False
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            self.api_error(e.message)
            return False
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            self.api_error(e.message)
            return False
        except stripe.error.StripeError as e:
            # Display a very generic error to the user
            self.api_error(e.message)
            return False
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("Unknown error occured")
            return False
