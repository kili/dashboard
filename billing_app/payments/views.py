from accounting import managers
#import base64
import billing
from billing_app.models import Card  # noqa
from billing_app.models import MobileMoneyNumber  # noqa
from billing_app.payments import forms as payment_forms  # noqa
from billing_app.payments import tables as payment_tables  # noqa
from django import template
from django.conf import settings
from django.core import urlresolvers
# from django.views import generic
from django.template.defaultfilters import linebreaks  # noqa
from django.template.defaultfilters import safe  # noqa
from django.utils.encoding import force_unicode
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


class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing/payments/index.html'
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


class PaymentViewBase(horizon_forms.ModalFormView):
    success_url = urlresolvers.reverse_lazy('horizon:billing:payments:index')
    template_name = 'billing/payments/payment_form_base.html'
    modal_header = 'Form'
    form_submit_url = None
    submit_button_label = 'Submit'
    help_text_template = None
    help_text = ' '

    def get_context_data(self, **kwargs):
        context = super(PaymentViewBase, self).get_context_data(**kwargs)
        context['form_submit_url'] = self.form_submit_url \
            or urlresolvers.resolve(self.request.path_info).view_name
        context['submit_button_label'] = self.submit_button_label
        context['help_text'] = self.get_help_text()
        context['modal_header'] = self.modal_header
        return context

    def get_help_text(self):
        help_text = ' '
        if self.help_text_template:
            tmpl = template.loader.get_template(self.help_text_template)
            context = template.RequestContext(self.request)
            help_text += tmpl.render(context)
        else:
            help_text += linebreaks(force_unicode(self.help_text))
        return safe(help_text)


class AddCardView(PaymentViewBase):
    form_class = payment_forms.AddCardForm
    template_name = 'billing/payments/add_card.html'
    modal_header = 'Add Debit/Credit Card'

    def get_context_data(self, **kwargs):
        context = super(AddCardView, self).get_context_data(**kwargs)
        context['stripe_obj'] = billing.get_integration('stripe')
        return context


class CardPayView(PaymentViewBase):
    form_class = payment_forms.CardPayForm
    help_text_template = 'billing/payments/_card_pay_help.html'
    modal_header = 'Add Funds'

    def get_context_data(self, **kwargs):
        context = super(CardPayView, self).get_context_data(**kwargs)
        return context


class AddMobileNumberView(PaymentViewBase):
    form_class = payment_forms.AddMobileNumberForm
    help_text_template = 'billing/payments/_add_number_help.html'
    modal_header = 'Add Mobile Number'

    def get_context_data(self, **kwargs):
        context = super(AddMobileNumberView, self).get_context_data(**kwargs)
        return context


class EnterTransactionCodeView(PaymentViewBase):
    form_class = payment_forms.MobileTransactionCodeForm
    help_text_template = \
        'billing/payments/_mobile_transaction_code_entry_help.html'
    modal_header = 'Enter Transaction Code'

    def get_context_data(self, **kwargs):
        context = super(
            EnterTransactionCodeView, self).get_context_data(**kwargs)
        return context
