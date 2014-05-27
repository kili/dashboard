import datetime

from billing import CreditCard, get_gateway, get_integration
from billing.gateway import CardNotSupported

from horizon import views

from .forms import CreditCardForm
#from .urls import stripe_obj
import pdb; pdb.set_trace()
stripe_obj = get_integration("stripe_example")


class IndexView(views.APIView):
    template_name = 'billing_app/payments/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

