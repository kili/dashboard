from openstack_dashboard.test.settings import *  # noqa

HORIZON_CONFIG['customization_module'] = 'customizations.loader'

INSTALLED_APPS += (
    'kili',
    'registration',
    'allauth',
    'allauth.account',
    'async',
    'accounting',
    'swingtix.bookkeeper',
    'resource_pricing',
    'resource_pricing.calculators.instance',
    'resource_pricing.calculators.volume',
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
                 'price_calculator': 'resource_pricing.calculators.instance'},
    'volume': {'id': 1,
               'price_calculator': 'resource_pricing.calculators.volume'},
    'network': {'id': 2,
                'price_calculator': 'resource_pricing.calculators.network'},
    'testtype1': {'id': 3,
                  'price_calculator': 'testcalculator1'},
}
