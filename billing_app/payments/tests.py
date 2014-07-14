import logging
import stripe

from django.db import IntegrityError
from django.conf import settings
from django.core.urlresolvers import reverse

from accounting.managers import AccountManager
from billing_app.models import Card
from django.test.client import RequestFactory  # noqa
from billing_app.models import MobileMoneyNumber
from billing_app.payments import views as payment_views
from django.contrib.auth import get_user_model
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
    # Unit tests for payments.

    def setUp(self):
        super(PaymentsTests, self).setUp()
        self.stripe = stripe
        self.stripe.api_key = settings.MERCHANT_SETTINGS['stripe']['API_KEY']
        self.am = AccountManager()
        self.card1_data = {'number': '4242424242424242',
                           'exp_month': 12,
                           'exp_year': 2016,
                           'cvc': '123'}
        self.card1_params = {
            'last4': '4242',
            'email': '123@test.com',
            'default': False,
            'tenant_id': '1'}

    def test_environment_sanity(self):
        # make sure our test environment is realy in TEST MODE

        self.assertTrue(settings.MERCHANT_TEST_MODE)
        self.assertTrue(
            "test" in
            settings.MERCHANT_SETTINGS['stripe']['API_KEY'])
        self.assertTrue(
            "test" in
            settings.MERCHANT_SETTINGS['stripe']['PUBLISHABLE_KEY'])

    # integration tests
    def test_add_card(self):
        card_token = self.stripe.Token.create(card=self.card1_data)
        card = Card.create(stripe_card_token=card_token.id,
                           **self.card1_params)
        self.assertEqual(card.default, True)

    def test_add_duplicate_card(self):
        card_token = self.stripe.Token.create(card=self.card1_data)
        Card.create(stripe_card_token=card_token.id, **self.card1_params)
        stripe.api_key = settings.MERCHANT_SETTINGS['stripe']['API_KEY']
        card_token = self.stripe.Token.create(card=self.card1_data)
        logging.disable(logging.exception)
        with self.assertRaises(IntegrityError):
            Card.create(stripe_card_token=card_token.id, **self.card1_params)

    def test_charge_user(self):
        card_token = self.stripe.Token.create(card=self.card1_data)
        Card.create(stripe_card_token=card_token.id,
                           **self.card1_params)
        formData = {'amount': 123123}
        self.client.post(reverse('horizon:billing:payments:add_funds'),
                         formData)
        self.assertEqual(
            self.am.get_user_account(
                self.card1_params['tenant_id']).balance(),
            123123)

    # Unit tests for payments.
    def test_me(self):
        self.assertTrue(1 + 1 == 2)

    def test_add_mobile_number(self):
        pass

    # k2 notification endpoint test
    def test_k2_notification(self):
        k2_notification_data
        response = k2_notify(k2_notification_data)
        self.assertTrue(json.loads(response.content)['status'] == u'01',
                        u'Unexpected k2 notification endpoint response')
        return True
