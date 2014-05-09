from openstack_dashboard.test.settings import *  # noqa

HORIZON_CONFIG['customization_module'] = 'customizations.loader'

INSTALLED_APPS += (
    'kili',
    'registration',
    'allauth',
    'allauth.account',
    'async',
)

CUSTOMIZATIONS = (
    'customizations.launch_instance.LaunchInstanceViewCustomizer',
)

ENV_NAME = "test"
