from billing_app.models import StripeCustomer
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import tables


class AddCard(tables.LinkAction):

    name = "Add Card"
    verbose_name = _("Add Credit / Debit Card")
    url = "payments/cards/add"
    classes = ("btn-create", "ajax-modal")
    ajax = True

    def single(self, table, request, object_id=None):
        self.allowed(request, None)
        return HttpResponse(self.render())


class AddFunds(tables.LinkAction):

    name = "Add Funds"
    verbose_name = _("$ Add Funds to Your Kili Account")
    url = "payments/cards/addfunds"
    classes = ("btn-success", "btn-lg", "ajax-modal")
    ajax = True

    def single(self, table, request, object_id=None):
        self.allowed(request, None)
        return HttpResponse(self.render())


class DeleteCard(tables.BatchAction):
    name = "DeleteCard"
    verbose_name = _("Delete Credit/Debit Card")
    ajax = True
    action_present = _("Delete")
    action_past = _("Deleted card")
    data_type_singular = _("Card")
    data_type_plural = _("Cards")
    classes = ('btn-danger', 'btn-terminate')

    def allowed(self, request, instance=None):
        return True

    def action(self, request, obj_id):
        return StripeCustomer.objects.delete_card(
            int(obj_id),
            request.user.id
        )


class MakeDefault(tables.BatchAction):
    name = "Make Default"
    verbose_name = _("Make this my default card")
    ajax = True
    action_present = _("Make Default")
    action_past = _("New Default")
    data_type_singular = _("Card")
    data_type_plural = _("Cards")
    classes = ("btn-enable",)

    def allowed(self, request, instance=None):
        return True

    def action(self, request, obj_id):
        StripeCustomer.objects.ensure_default(
            int(obj_id),
            request.user.id
        )


class StripeCardCustomerTable(tables.DataTable):

    name = tables.Column("name",
                         verbose_name=_("Card Name"))
    default = tables.Column("default",
                            verbose_name=_("Is Default"))

    class Meta:
        name = "Cards"
        verbose_name = _("Your Credit/Debit Cards")
        table_actions = (AddFunds, AddCard, DeleteCard)
        row_actions = (DeleteCard, MakeDefault)
