from django.utils.translation import ugettext_lazy as _
import horizon
from openstack_dashboard.dashboards.admin import dashboard


class Pricing(horizon.Panel):
    slug = 'pricing'
    name = _('Pricing')
    permissions = ('openstack.roles.admin',)


dashboard.Admin.register(Pricing)
