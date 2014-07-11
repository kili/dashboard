from accounting import transactions
import billing
from billing.forms import stripe_forms  # noqa
from billing_app.models import K2RawData
from billing_app.models import Card
from billing_app.models import MobileMoneyNumber
import decimal
from django.conf import settings  # noqa
from django.core.exceptions import ObjectDoesNotExist  # noqa
from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.db import IntegrityError
from django.core.exceptions import FieldError
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import messages


stripe = billing.get_gateway("stripe").stripe


class AddCardForm(horizon_forms.SelfHandlingForm, stripe_forms.StripeForm):

    last4 = horizon_forms.CharField(widget=horizon_forms.HiddenInput())
    default = horizon_forms.BooleanField(
        label=_("Make this my Default Card"),
        required=False
    )
    stripe_card_token = horizon_forms.CharField(
        widget=horizon_forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        self.fields.pop('amount')

    def handle(self, request, data):
        try:
            card = Card.create(last4=data['last4'],
                               default=data['default'],
                               tenant_id=request.user.tenant_id,
                               stripe_card_token=data['stripe_card_token'],
                               email=request.user.username)
            messages.success(
                request,
                _('Credit card "%s" has been tied to your account.') %
                card.name)
            return True
        except (FieldError, ValidationError, IntegrityError) as e:
            self.api_error(e.message)
        except Exception:
            exceptions.handle(request, ignore=True)


class CardPayForm(horizon_forms.SelfHandlingForm):

    amount = horizon_forms.DecimalField(label=_("Amount (In US Dollars)"),
                                required=True,
                                min_value=decimal.Decimal('15'))

    def __init__(self, *args, **kwargs):
        super(CardPayForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not Card.objects.filter(
                tenant_id__exact=self.request.user.tenant_id,
                default=True).exists():
            raise ValidationError(_("Could not find default billing card. "
                                    "Please select one of your cards as "
                                    "the default for billing."))
        return super(CardPayForm, self).clean()

    def handle(self, request, data):
        try:
            # register charge on stripe
            stripe.Charge.create(
                amount=data['amount'] * 100,  # stripe expects amount in cents.
                currency="usd",
                customer=Card.objects.get(
                    tenant_id__exact=self.request.user.tenant_id,
                    default=True).stripe_customer_id
            )

            # credit user account
            transactions.UserTransactions().receive_user_payment(
                request.user.tenant_id,
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
        except (stripe.error.CardError,
                stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
            self.api_error(e.message)
            return False
        except django_forms.ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("Unknown error occured")
            return False


class AddMobileNumberForm(horizon_forms.SelfHandlingForm):

    mobile_number = horizon_forms.CharField(
        label=_("Enter an M-Pesa enabled number"),
        required=True,
        widget=horizon_forms.NumberInput(),
        min_length=10,
        max_length=10)

    def handle(self, request, data):
        try:
            MobileMoneyNumber.create(number=data['mobile_number'],
                                     tenant_id=request.user.tenant_id)
            messages.success(
                request,
                _('M-Pesa Number "%s" has been tied to your account.')
                % data['mobile_number']
            )

            return True
        except django_forms.ValidationError as e:
            self.api_error(e.messages[0])
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("An error occured while adding your number. "
                           "Please try again later.")
        return False


class MobileTransactionCodeForm(horizon_forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(MobileTransactionCodeForm, self).__init__(*args, **kwargs)

    transaction_ref = horizon_forms.CharField(
        label=_("Enter mobile money transaction code"),
        required=True
    )

    def handle(self, request, data):
        try:
            transaction = K2RawData.objects.get(
                transaction_reference=data['transaction_ref'],
                claimed=False)

            usd_amount = transaction.amount / settings.K2_KES_USD_RATE
            user_transactions = transactions.UserTransactions()

            user_transactions.receive_user_payment(
                request.user.tenant_id,
                "KOPOKOPO", usd_amount,
                ("Claimed mobile money payment."
                " Transaction ref %s" % data['transaction_ref']))

            transaction.claimed = True
            transaction.save()

            messages.success(
                request,
                ("You successfully claimed mobile money payment with "
                "transaction ref %s" % data['transaction_ref']))
            return True
        except ObjectDoesNotExist:
            self.api_error("The transaction code you entered is invalid.")
            return False
        except django_forms.ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            return False


class K2Form(django_forms.ModelForm):
    service_name = django_forms.CharField(max_length=64, required=False)
    transaction_type = django_forms.CharField(max_length=64, required=False)
    account_number = django_forms.CharField(max_length=64, required=False)
    middle_name = django_forms.CharField(max_length=64, required=False)
    last_name = django_forms.CharField(max_length=64, required=False)
    transaction_timestamp = django_forms.DateTimeField(required=True,
        input_formats=['%Y-%m-%dT%H:%M:%SZ'])
    amount = django_forms.DecimalField(required=True)
    claimed = django_forms.BooleanField(required=False)

    class Meta:
        model = K2RawData
        fields = '__all__'
