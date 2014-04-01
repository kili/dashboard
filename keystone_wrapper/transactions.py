from django.conf import settings
from keystoneclient.v2_0.client import Client
from keystone_wrapper.domain import TransactionDomainCreator
from keystone_wrapper.project import TransactionProjectCreator
from keystone_wrapper.tenant import TransactionTenantCreator
from keystone_wrapper.group import TransactionGroupCreator
from keystone_wrapper.user import TransactionUserCreator
from keystone_wrapper.roles import TransactionDefaultRoles


class CreateUserTransaction():

    def __init__(self):
        self.client = Client(
            token=settings.KEYSTONE_TOKEN,
            endpoint=settings.KEYSTONE_URL)

    def create_user(self, **kwargs):
        tenant_name = kwargs['tenant_name']
        group_name = kwargs['group_name']
        user_name = kwargs['user_name']
        password = kwargs['password']

        with TransactionTenantCreator(
                client=self.client, tenant_name=tenant_name) as tenant,\
                TransactionUserCreator(
                    client=self.client, user_name=user_name, password=password,
                    tenant_id=tenant.id) as user,\
                TransactionDefaultRoles(
                    client=self.client, user_id=user.id, tenant_id=tenant.id):
            if user.id is None:
                raise Exception("couldn't create keystone user")
            return (tenant.id, user.id)
