from accounting import managers
#import base64
import billing
from billing_app.models import Card  # noqa
from billing_app.models import MobileMoneyNumber  # noqa
from billing_app.payments import forms as payment_forms  # noqa
from billing_app.payments import tables as payment_tables  # noqa
from django.conf import settings
from django.core import urlresolvers
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


stripe_obj = billing.get_integration("stripe")


class MobileNumberTableEntry(object):

    def __init__(self, id, number):
        self.id = id
        self.number = number
        self.name = number


class CardTableEntry(object):

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
