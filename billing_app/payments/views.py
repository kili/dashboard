import billing
from billing_app.models import StripeCustomer  # noqa
from billing_app.payments import forms as payment_forms  # noqa
from billing_app.payments import tables as card_tables  # noqa
# from django.core.urlresolvers import reverse_lazy
from horizon import exceptions
from horizon import forms
from horizon import tables as horizon_tables  # noqa


stripe_obj = billing.get_integration("stripe")


class CardTableEntry():

    def __init__(self, id, name, is_default):
        self.id = id
        self.name = name
        self.default = is_default


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/payments/index.html'
    table_class = card_tables.StripeCardCustomerTable

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['stripe_obj'] = stripe_obj
        return context

    def get_data(self):
        self._more = False
        try:
            cards = [CardTableEntry(
                     x.id,
                     x.name,
                     x.is_default)
                     for x in StripeCustomer.objects.filter(
                     keystone_id__exact=self.request.user.id).order_by(
                         'is_default', 'id').reverse()]
        except Exception:
            cards = []
            exceptions.handle(self.request,
                              _('Unable to retrieve cards.'))
        return cards


class AddCardView(forms.ModalFormView):
    form_class = payment_forms.AddCardForm
    template_name = "billing_app/payments/add_card.html"
    success_url = "/billing/"

    def get_context_data(self, **kwargs):
        context = super(AddCardView, self).get_context_data(**kwargs)
        context['stripe_obj'] = stripe_obj
        return context


class CardPayView(forms.ModalFormView):
    form_class = payment_forms.CardPayForm
    template_name = "billing_app/payments/card_pay.html"
    success_url = "/billing/"

    def get_context_data(self, **kwargs):
        context = super(CardPayView, self).get_context_data(**kwargs)
        context['stripe_obj'] = stripe_obj
        return context
