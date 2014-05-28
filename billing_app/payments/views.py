from billing import get_integration
from horizon import views


stripe_obj = get_integration("stripe")


class IndexView(views.APIView):
    template_name = 'billing_app/payments/index.html'

    def get_data(self, request, context, *args, **kwargs):
        status = request.GET.get("status")
        stripe_obj.add_field("amount", 100)
        stripe_vars = {'title': 'Stripe.js',
                     "stripe_obj": stripe_obj,
                     "status": status}
        context.update(stripe_vars)
        return context
