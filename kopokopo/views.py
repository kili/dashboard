from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView  # noqa
from kopokopo import forms


class KopoKopoView(FormView):
    form_class = forms.KopoKopoForm
    template_name = "api.html"

    def post(self, request, *args, **kwargs):
        response = {'status': "01",
                    'description': "Accepted"}
        http_response = HttpResponse(
            json.dumps(response),
            content_type='application/json')

        form = self.get_form(self.form_class)

        # validate notification data
        if not form.is_valid():
            response['status'] = "03"
            response['description'] = (
                "Invalid payment data %s" % json.dumps(form.errors))
            http_response.content = json.dumps(response)
            return http_response

        data = form.save(commit=False)

        # generate base string for hash creation
        # TODO(james): HMAC verification

        # data is good, now for some debits and credits
        # check if sender number is known
        sender_phone = data.sender_phone.replace('+254', '0')

        user_transactions = transactions.UserTransactions()

        try:
            tenant_number = MobileMoneyNumber.objects.get(
                number=sender_phone)
            usd_amount = data.amount / settings.K2_KES_USD_RATE
            user_transactions.receive_user_payment(
                tenant_number.tenant_id,
                "KOPOKOPO", usd_amount,
                ("Received mobile money payment."
                 " Transaction ref %s"
                 % data.transaction_reference))
            data.claimed = True
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            data.claimed = False

        data.save()
        return http_response

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(KopoKopoView, self).dispatch(*args, **kwargs)
