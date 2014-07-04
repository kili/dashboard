from openstack_dashboard.test import helpers as test  # noqa


class PaymentsTests(test.TestCase):
    # Unit tests for payments.
    def test_me(self):
        self.assertTrue(1 + 1 != 2)
