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
