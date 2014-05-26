from django.utils.translation import ugettext_lazy as _

import horizon

class Billing_App(horizon.Dashboard):
    name = _("Billing")
    slug = "billing"
    panels = ('payments','history')  # Add your panels here.
    default_panel = 'payments'  # Specify the slug of the dashboard's default panel.


horizon.register(Billing_App)
