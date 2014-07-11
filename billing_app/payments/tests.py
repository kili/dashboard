import logging
import stripe

from django.db import IntegrityError
from django.conf import settings
from django.core.urlresolvers import reverse
from openstack_dashboard.test import helpers as test

from accounting.managers import AccountManager
from billing_app.models import Card


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
