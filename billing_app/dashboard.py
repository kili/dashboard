from django.utils.translation import ugettext_lazy as _

import horizon


class Billing_App(horizon.Dashboard):
    name = _("Billing")
    slug = "billing"
    panels = ('payments', 'history', 'usage')
    default_panel = 'payments'


horizon.register(Billing_App)
