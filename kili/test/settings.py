from openstack_dashboard.test.settings import *  # noqa

ROOT_URLCONF = 'kili.urls'

HORIZON_CONFIG['customization_module'] = 'customizations.loader'

INSTALLED_APPS += (
    'kili',
    'kopokopo',
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
    'resource_pricing.calculators',
    'project_billing',
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
ACCOUNTING_USER_ACCOUNT_FORMAT = {"regex": "^USER_[a-f0-9]+$",
                                  "format": "USER_{0}"}

ACCOUNTING_VALID_ACCOUNTS = ACCOUNTING_ASSET_SOURCES[:]
ACCOUNTING_VALID_ACCOUNTS.append(ACCOUNTING_PROMOTIONS_ACCOUNT)
ACCOUNTING_VALID_ACCOUNTS.append(ACCOUNTING_REVENUE_ACCOUNT)
ACCOUNTING_VALID_ACCOUNTS.append(ACCOUNTING_USER_ACCOUNT_FORMAT["regex"])

ACCOUNTING_CREDIT_NEGATIVE_ACCOUNTS = ACCOUNTING_ASSET_SOURCES[:]
ACCOUNTING_CREDIT_NEGATIVE_ACCOUNTS.append(ACCOUNTING_PROMOTIONS_ACCOUNT)

BILLABLE_RESOURCE_TYPES = {
    'instance': {'period_length': 10},
    'volume': {'period_length': 10},
    'testtype1': {'period_length': 10}}

MERCHANT_TEST_MODE = True
MERCHANT_SETTINGS = {
    "stripe": {
        "API_KEY": "sk_test_B6lIS1GVOAL8SenO3DeLlCQN",
        "PUBLISHABLE_KEY": "pk_test_GV1PYwn9wFTVQ0yHyVEWT6Ib",
    }
}

MINIMUM_BALANCE = 0

K2_API_KEY = '1234567890'
K2_AUTHORIZATION_HEADER = 'HTTP_AUTHORIZATION'
K2_KES_USD_RATE = 88

KOPOKOPO_USERNAME = 'K2USER'
KOPOKOPO_PASSWORD = 'K2PASS'
