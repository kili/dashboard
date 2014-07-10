from accounting import transactions
import billing
from billing.forms import stripe_forms
from billing_app.models import Card
from billing_app.models import MobileMoneyNumber
import decimal
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.core.exceptions import FieldError
from horizon import exceptions
from horizon import forms
from horizon import messages


stripe = billing.get_gateway("stripe").stripe


class AddCardForm(forms.SelfHandlingForm, stripe_forms.StripeForm):

    last4 = forms.CharField(widget=forms.HiddenInput())
    default = forms.BooleanField(
        label=_("Make this my Default Card"),
        required=False
    )
    stripe_card_token = forms.CharField(widget=forms.HiddenInput())

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
            card.save()
            messages.success(
                request,
                _('Credit card "%s" has been tied to your account.') %
                card.name)
            return True
        except (FieldError, ValidationError) as e:
            self.api_error(e.message)
        except Exception:
            exceptions.handle(request, ignore=True)


class CardPayForm(forms.SelfHandlingForm):

    amount = forms.DecimalField(label=_("Amount (In US Dollars)"),
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
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("Unknown error occured")
            return False


class AddMobileNumberForm(forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(AddMobileNumberForm, self).__init__(*args, **kwargs)

    mobile_number = forms.CharField(label=_("Enter an M-Pesa enabled number"),
                                    required=True,
                                    widget=forms.NumberInput(),
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


class MobileTransactionCodeForm(forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(MobileTransactionCodeForm, self).__init__(*args, **kwargs)

    transaction_code = forms.IntegerField(
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
