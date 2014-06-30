from openstack_dashboard.test.settings import *  # noqa

HORIZON_CONFIG['customization_module'] = 'customizations.loader'

INSTALLED_APPS += (
    'kili',
    'billing_app',
    'billing',
    'stripe',
    'registration',
    'allauth',
    'allauth.account',
    'async',
    'accounting',
    'swingtix.bookkeeper',
    'resource_pricing',
    'resource_pricing.calculators.instance',
    'resource_pricing.calculators.volume',
    'user_billing',
    'user_billing.metering',
    'user_billing.metering.ceilometer',
)

CUSTOMIZATIONS = (
    'customizations.launch_instance.LaunchInstanceViewCustomizer',
)

ENV_NAME = "test"

ACCOUNTING_BOOKS = {
    "USD": "user_accounts_usd"
}
ACCOUNTING_ASSET_SOURCES = [
    "STRIPE",
    "KOPOKOPO",
]
ACCOUNTING_PROMOTIONS_ACCOUNT = "PROMOTIONS"
ACCOUNTING_REVENUE_ACCOUNT = "REVENUE"
ACCOUNTING_USER_ACCOUNT_FORMAT = {"regex": "USER_[a-f0-9]{32}",
                                  "format": "USER_{0}"}

BILLABLE_RESOURCE_TYPES = {
    'instance': {'id': 0,
                 'price_calculator': 'resource_pricing.calculators.instance',
                 'period_length': 10,
                 'meters': ['instance:MIcro',
                            'instance:Small',
                            'instance:Medium',
                            'instance:High CPU',
                            'instance:LArge',
                            'instance:High RAM',
                            'instance:Extra Large']},
    'volume': {'id': 1,
               'period_length': 10,
               'price_calculator': 'resource_pricing.calculators.volume'},
    'network': {'id': 2,
                'period_length': 10,
                'price_calculator': 'resource_pricing.calculators.network'},
    'testtype1': {'id': 3,
                  'period_length': 10,
                  'price_calculator': 'testcalculator1'},
}

MERCHANT_TEST_MODE = True
MERCHANT_SETTINGS = {
    "stripe": {
        "API_KEY": "sk_test_B6lIS1GVOAL8SenO3DeLlCQN",
        "PUBLISHABLE_KEY": "pk_test_GV1PYwn9wFTVQ0yHyVEWT6Ib",
    }
}

K2_AUTHORIZATION_HEADER = 'HTTP_AUTHORIZATION'
