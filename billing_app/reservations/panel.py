'''
from django.utils.translation import ugettext_lazy as _

import horizon

from billing_app import dashboard


class Reservations(horizon.Panel):
    name = _("Reservations")
    slug = "reservations"


dashboard.Billing_App.register(Reservations)
'''
