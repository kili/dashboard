from django.utils.translation import ugettext_lazy as _
from horizon import tables


class AddCard(tables.LinkAction):

    name = "Add Card"
    verbose_name = _("Add Credit/Debit Card")
    url = "payments/cards/add"
    classes = ("btn-create", "ajax-modal")
    ajax = True
    
    def single(self, table, request, object_id=None):
        self.allowed(request, None)
        return HttpResponse(self.render())

class DeleteCard(tables.LinkAction):

    name = "Delete Card"
    verbose_name = _("Delete Credit/Debit Card")
    url = "payments/cards/delete"
    classes = ("btn-delete", "ajax-modal")
    ajax = True

class MakeDefault(tables.LinkAction):
    
    name = "Make Default"
    verbose_name = _("Make this my default card")
    url = "payments/cards/makedefault"
    classes = ("btn-enable", "ajax-modal")
    ajax = True

class StripeCardCustomerTable(tables.DataTable):
    
    name = tables.Column("Card Name")
    default = tables.Column("Is Default")
    
    class Meta:
        name = "Cards"
        verbose_name = _("Your Credit/Debit Cards")
        #status_columns = ["status", "task"]
        table_actions = (AddCard,)
        row_actions = (DeleteCard, MakeDefault)
