import billing
from django.utils.translation import ugettext_lazy as _
from billing.forms import stripe_forms
from billing_app.models import StripeCustomer
from django.forms import ValidationError
from horizon import exceptions
from horizon import forms


stripe = billing.get_gateway("stripe").stripe

class AddCardForm(stripe_forms.StripeForm, forms.SelfHandlingForm):
    def __init__(self, *args, **kwargs):
        super (AddCardForm, self).__init__(*args,**kwargs)
        self.fields.pop('amount') 

    card_name = forms.CharField(label=_("Card Name"),
                                required=True)
    make_default = forms.BooleanField(label=_("Make this my Default Card"),
                                         required=False)
    stripe_card_token = forms.CharField(widget=forms.HiddenInput())

    def handle(self, request, data):
        #import pdb; pdb.set_trace()
        try:
            # Create a Customer
            stripe_customer = stripe.Customer.create(
                        card=data['stripe_card_token'],
                        description=data['card_name']
                    )
            StripeCustomer.objects.create_stripe_customer(
                        data['card_name'],
                        data['make_default'],
                        request.user.id,
                        stripe_customer.id
                    )
            return True 
        except stripe.InvalidRequestError as e:
            self.api_error(e.message)
            return False
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error("Unknown error")
            return False
