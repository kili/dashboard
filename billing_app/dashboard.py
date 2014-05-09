from django.utils.translation import ugettext_lazy as _

import horizon
import payments

class Billing_App(horizon.Dashboard):
    name = _("Billing_App")
    slug = "billing_app"
    panels = (payments)  # Add your panels here.
    default_panel = 'payments'  # Specify the slug of the dashboard's default panel.


horizon.register(Billing_App)
