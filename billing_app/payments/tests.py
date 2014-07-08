from openstack_dashboard.test import helpers as test  # noqa
from django.test.client import RequestFactory  # noqa
from billing_app.payments import views as payment_views
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
import json


TENANT_ID = "t_abc123"

TEST_USER = get_user_model()()
TEST_USER.tenant_id = TENANT_ID

k2_notification_data = {
    'first_name': 'John', 'last_name': 'Doe', 
    'transaction_timestamp': '2014-06-25T19:35:57Z', 
    'internal_transaction_id': '123456', 'service_name': 'M-PESA',
    'transaction_type': 'buygoods', 'currency': 'Ksh',
    'amount': '1100', 'transaction_reference': 'XXXXXXXX',
    'account_number': 'Not Listed',
    'signature': 'TEST FOR THIS WHEN K2 BEHAVES',
    'sender_phone': '+254720000000',
    'username': 'K2USER', 
    'password': 'K2PASS',
    'business_number': '333997'}

k2_endpoint_url = \
    reverse('horizon:billing:payments:k2_version2_endpoint')
add_number_url = \
    reverse('horizon:billing:payments:add_number')

def k2_notify(k2_data):
    k2view = payment_views.K2_v2(
        **{'request': RequestFactory().post(k2_endpoint_url, k2_data)})
    return k2view.dispatch(request)

def add_mobile_number(mobile_number):
    request = RequestFactory().post(
        RequestFactory().post(add_number_url,
        {'mobile_number':mobile_number}))
    request.user = TEST_USER 
    mobile_number_view = payment_views.AddMobileNumberView(**{'request': request})
    return mobile_number_view.dispatch(request)

class PaymentsTests(test.TestCase):

    def test_add_mobile_number(self):
        add_mobile_number('0720123456')
        MobileMoneyNumber.objects.filter(mobile_number = '0720123456')
        return true

    #k2 notification endpoint test
    def test_k2_notification(self):
        valid_k2_data = k2_notification_data
        response = k2_notify(k2_notification_data)
        self.assert(json.loads(response.content)['status'] == u'01')
        return true
