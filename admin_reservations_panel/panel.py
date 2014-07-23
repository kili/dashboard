from django.utils.translation import ugettext_lazy as _
import horizon
from openstack_dashboard.dashboards.admin import dashboard

class AdminReservationsPanel(horizon.Panel):
    name = _("Reservations")
    slug = "reservations"


dashboard.Admin.register(AdminReservationsPanel)
