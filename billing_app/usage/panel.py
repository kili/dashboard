from django.utils.translation import ugettext_lazy as _

import horizon

from billing_app import dashboard


class Usage(horizon.Panel):
    name = _("Usage")
    slug = "usage"


dashboard.Billing_App.register(Usage)
