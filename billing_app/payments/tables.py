from billing_app import models
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tables
import logging


LOG = logging.getLogger(__name__)


class AddCard(tables.LinkAction):

    name = "Add Card"
    verbose_name = _("Add Credit / Debit Card")
    url = "horizon:billing:payments:add_card"
    classes = ('btn-create', 'ajax-modal')
    ajax = True

    def single(self, table, request, object_id=None):
        return HttpResponse(self.render())


class AddFunds(tables.LinkAction):

    name = "Add Funds"
    verbose_name = _("Add Funds to Your Account")
    url = "horizon:billing:payments:add_funds"
    classes = ('btn-success', 'btn-large', 'ajax-modal')
    ajax = True

    def single(self, table, request, object_id=None):
        return HttpResponse(self.render())

    def allowed(self, request, datum):
        return bool(self.table.data)


class DeleteCard(tables.DeleteAction):
    name = "DeleteCard"
    verbose_name = _("Delete Credit/Debit Card")
    ajax = True
    action_present = _("Delete")
    action_past = _("Deleted card")
    data_type_singular = _("Card")
    data_type_plural = _("Cards")
    classes = ('btn-danger', 'btn-terminate')

    def delete(self, request, card_id):
        models.Card.objects.filter(pk=card_id).delete()


class MakeDefault(tables.BatchAction):
    name = "Make Default"
    verbose_name = _("Make this my default card")
    ajax = True
    action_present = _("Set as Default")
    action_past = _("New Default")
    data_type_singular = _("Card")
    data_type_plural = _("Cards")
    classes = ("btn-enable",)

    def action(self, request, obj_id):
        models.Card.objects.get(pk=obj_id).make_default()


class StripeCardCustomerTable(tables.DataTable):

    name = tables.Column("name",
                         verbose_name=_("Card"))
    default = tables.Column("default",
                            verbose_name=_("Default"))

    class Meta:
        name = "cards"
        verbose_name = _("Your Credit/Debit Cards")
        table_actions = (AddFunds, AddCard)
        row_actions = (DeleteCard, MakeDefault)


# mobile money
class AddMobileMoneyNumber(tables.LinkAction):

    name = "Add Number"
    verbose_name = _("Add M-Pesa Enabled Number")
    url = "horizon:billing:payments:add_number"
    classes = ('btn-create', 'ajax-modal')
    ajax = True

    def single(self, table, request, object_id=None):
        return HttpResponse(self.render())


class EnterCode(tables.LinkAction):

    name = "Enter Transaction Code"
    verbose_name = _("Add funds via Transaction Code")
    url = "horizon:billing:payments:enter_transaction_code"
    classes = ('btn-success', 'ajax-modal')
    ajax = True

    def single(self, table, request, object_id=None):
        return HttpResponse(self.render())


class DeleteMobileMoneyNumber(tables.DeleteAction):
    name = "DeleteNumber"
    verbose_name = _("Delete")
    ajax = True
    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Number")
    data_type_plural = _("Nubers")
    classes = ('btn-danger', 'btn-terminate')

    def delete(self, request, number_id):
        result = models.MobileMoneyNumber.objects.delete_number(
            int(number_id),
            request.user.tenant_id
        )
        if not result[0]:
            LOG.error(
                'Could not delete mobile number: %s' % (number_id, result[1])
            )
            raise exceptions.Conflict(result[1])


class MobileMoneyTable(tables.DataTable):

    name = tables.Column("number",
                         verbose_name=_("Number"))

    class Meta:
        name = "mobile_money"
        verbose_name = _("Your Mobile Money Numbers")
        table_actions = (AddMobileMoneyNumber, EnterCode)
        row_actions = (DeleteMobileMoneyNumber, )
