from accounting import transactions
import billing
from billing.forms import stripe_forms  # noqa
from billing_app.models import k2_raw_data
from billing_app.models import MobileMoneyNumber
from billing_app.models import StripeCustomer
import decimal
from django import forms as django_forms
from django.forms import ValidationError  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import messages


stripe = billing.get_gateway("stripe").stripe


class AddCardForm(stripe_forms.StripeForm, horizon_forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        self.fields.pop('amount')

    card_name = horizon_forms.CharField(widget=horizon_forms.HiddenInput())
    make_default = horizon_forms.BooleanField(
        label=_("Make this my Default Card"),
        required=False
    )
    stripe_card_token = horizon_forms.CharField(
        widget=horizon_forms.HiddenInput())

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


class CardPayForm(horizon_forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(CardPayForm, self).__init__(*args, **kwargs)

    amount = horizon_forms.DecimalField(label=_("Amount (In US Dollars)"),
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
            ut.receive_user_payment(request.user.tenant_id,
                                    "STRIPE",
                                    data['amount'],
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


class AddMobileNumberForm(horizon_forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(AddMobileNumberForm, self).__init__(*args, **kwargs)

    mobile_number = horizon_forms.CharField(
        label=_("Enter an M-Pesa enabled number"),
        required=True,
        widget=horizon_forms.NumberInput(),
        min_length=10,
        max_length=10)

    def handle(self, request, data):
        try:
            result = MobileMoneyNumber.objects.add_number(
                data['mobile_number'],
                request.user.id
            )
            if not result[0]:
                raise ValidationError(result[1])

            messages.success(
                request,
                _('M-Pesa Number "%s" has been tied to your account.')
                % data['mobile_number']
            )
            return True
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("An error occured while adding your number. "
                           "Please try again later.")
            return False


class MobileTransactionCodeForm(horizon_forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(MobileTransactionCodeForm, self).__init__(*args, **kwargs)

    transaction_code = horizon_forms.IntegerField(
        label=_("Enter mobile money transaction code"),
        required=True
    )

    def handle(self, request, data):
        try:
            result = MobileMoneyNumber.objects.add_number(
                data['mobile_number'],
                request.user.id
            )
            if not result[0]:
                raise ValidationError(result[1])

            messages.success(
                request,
                _('M-Pesa Number "%s" has been tied to your account.')
                % data['mobile_number']
            )
            return True
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("An error occured while adding your number. "
                           "Please try again later.")
            return False


class K2Form(django_forms.ModelForm):
    service_name = django_forms.CharField(max_length=64, required=False)
    transaction_type = django_forms.CharField(max_length=64, required=False)
    account_number = django_forms.CharField(max_length=64, required=False)
    middle_name = django_forms.CharField(max_length=64, required=False)
    last_name = django_forms.CharField(max_length=64, required=False)

    class Meta:
        model = k2_raw_data
        fields = '__all__'
