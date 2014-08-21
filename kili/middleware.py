from accounting import managers
from django.core import urlresolvers
from django.conf import settings
from django.http import HttpResponseRedirect
from horizon import messages


class PaywallMiddleware(object):

    def __init__(self, *args, **kwargs):
        self.account_manager = managers.AccountManager()

    def process_request(self, request):
        if request.user.is_anonymous():
            return

        if (request.user.tenant_name in settings.PAYWALL_EXEMPT
        or urlresolvers.resolve(request.path).view_name
        not in settings.PAYWALL_LOOKOUT_VIEWS):
            return

        if not self.account_manager.has_sufficient_balance(
                request.user.tenant_id):
            messages.error(request,
                u'You need at least {} USD in order to access that resource!'.
                format(settings.MINIMUM_BALANCE))
            return HttpResponseRedirect(
                urlresolvers.reverse('horizon:billing:payments:index'))
