from accounting import managers
from accounting import transactions
#import base64
import billing
from billing_app.models import Card  # noqa
from billing_app.models import MobileMoneyNumber  # noqa
from billing_app.payments import forms as payment_forms  # noqa
from billing_app.payments import tables as payment_tables  # noqa
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from django.http import HttpResponse
# from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt  # noqa
from django.views.generic.edit import FormView  # noqa
#import hashlib
#import hmac
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import messages
from horizon import tables as horizon_tables  # noqa
import json


stripe_obj = billing.get_integration("stripe")


class MobileNumberTableEntry():

    def __init__(self, id, number):
        self.id = id
        self.number = number
        self.name = number


class CardTableEntry():

    def __init__(self, id, name, default):
        self.id = id
        self.name = name
        self.default = default


class PaymentViewBase(horizon_forms.ModalFormView):
    success_url = urlresolvers.reverse_lazy('horizon:billing:payments:index')


class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing_app/payments/index.html'
    table_classes = (payment_tables.StripeCardCustomerTable,
                     payment_tables.MobileMoneyTable)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['stripe_obj'] = billing.get_integration('stripe')
        if not managers.AccountManager().has_sufficient_balance(
                self.request.user.tenant_id):
            messages.warning(
                self.request,
                u'You need at least {0} USD to launch an instance'.
                format(settings.MINIMUM_BALANCE))
        return context

    def get_mobile_money_data(self):
        try:
            return [MobileNumberTableEntry(x.id, x.number)
                    for x in MobileMoneyNumber.objects.filter(
                    tenant_id__exact=self.request.user.tenant_id)]
        except Exception:
            exceptions.handle(self.request, _('Unable to retrieve numbers.'))
            return []

    def get_cards_data(self):
        try:
            cards = [CardTableEntry(
                     x.id,
                     x.name,
                     x.default)
                     for x in Card.objects.filter(
                     tenant_id__exact=self.request.user.tenant_id).order_by(
                         'default', 'id').reverse()]
        except Exception:
            cards = []
            exceptions.handle(self.request,
                              _('Unable to retrieve cards.'))
        return cards


class AddCardView(PaymentViewBase):
    form_class = payment_forms.AddCardForm
    template_name = "billing_app/payments/add_card.html"

    def get_context_data(self, **kwargs):
        context = super(AddCardView, self).get_context_data(**kwargs)
        context['stripe_obj'] = billing.get_integration('stripe')
        return context


class CardPayView(PaymentViewBase):
    form_class = payment_forms.CardPayForm
    template_name = "billing_app/payments/card_pay.html"

    def get_context_data(self, **kwargs):
        context = super(CardPayView, self).get_context_data(**kwargs)
        context['stripe_obj'] = billing.get_integration('stripe')
        return context


class AddMobileNumberView(PaymentViewBase):
    form_class = payment_forms.AddMobileNumberForm
    template_name = "billing_app/payments/add_number.html"

    def get_context_data(self, **kwargs):
        context = super(AddMobileNumberView, self).get_context_data(**kwargs)
        context['stripe_obj'] = stripe_obj
        return context


class EnterTransactionCodeView(PaymentViewBase):
    form_class = payment_forms.MobileTransactionCodeForm
    template_name = "billing_app/payments/mobile_transaction_code_entry.html"

    def get_context_data(self, **kwargs):
        context = super(
            EnterTransactionCodeView, self).get_context_data(**kwargs)
        context['stripe_obj'] = stripe_obj
        return context


class K2_v2(FormView):
    form_class = payment_forms.K2Form
    template_name = "billing_app/payments/k2v2.html"

    def post(self, request, *args, **kwargs):
        k2_response = {'status': "01",
                       'description': "Accepted"}
        http_response = HttpResponse(
            json.dumps(k2_response),
            content_type='application/json')

        k2_form = self.get_form(self.form_class)

        # validate notification data
        if not k2_form.is_valid():
            k2_response['status'] = "03"
            k2_response['description'] = (
                "Invalid payment data %s" % json.dumps(k2_form.errors))
            http_response.content = json.dumps(k2_response)
            return http_response

        k2_data = k2_form.save(commit=False)

        # generate base string for hash creation
        # TODO(james): HMAC verification

        # k2_data is good, now for some debits and credits
        # check if sender number is known
        sender_phone = k2_data.sender_phone.replace('+254', '0')

        user_transactions = transactions.UserTransactions()

        try:
            tenant_number = MobileMoneyNumber.objects.get(
                number=sender_phone)
            usd_amount = k2_data.amount / settings.K2_KES_USD_RATE
            user_transactions.receive_user_payment(
                tenant_number.tenant_id,
                "KOPOKOPO", usd_amount,
                ("Received mobile money payment."
                 " Transaction ref %s"
                 % k2_data.transaction_reference))
            k2_data.claimed = True
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            k2_data.claimed = False

        k2_data.save()
        return http_response

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(K2_v2, self).dispatch(*args, **kwargs)
