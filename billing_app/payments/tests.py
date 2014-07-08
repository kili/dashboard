#from billing_app.models import K2RawData
from billing_app.models import MobileMoneyNumber
from billing_app.payments import views as payment_views
#from billing_app.models import StripeCustomer
from django.contrib.auth import get_user_model  # noqa
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory  # noqa
import json
from openstack_dashboard.test import helpers as test  # noqa


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
    request = RequestFactory().post(k2_endpoint_url, k2_data)
    k2view = payment_views.K2_v2(
        **{'request': request})
    return k2view.dispatch(request)


def add_mobile_number(mobile_number):
    MobileMoneyNumber.objects.add_number(
        mobile_number,
        TEST_USER.tenant_id
    )


class PaymentsTests(test.TestCase):

    def test_add_mobile_number(self):
        pass

    # k2 notification endpoint test
    def test_k2_notification(self):
        k2_notification_data
        response = k2_notify(k2_notification_data)
        self.assertTrue(json.loads(response.content)['status'] == u'01',
                        u'Unexpected k2 notification endpoint response')
        return True
