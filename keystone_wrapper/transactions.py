from keystone_wrapper.client import KeystoneClient
from keystone_wrapper.roles import TransactionDefaultRoles
from keystone_wrapper.tenant import TransactionTenantCreator
from keystone_wrapper.user import TransactionUserCreator


class CreateUserTransaction():

    def __init__(self):
        self.client = KeystoneClient.get_client()

    def create_user(self, **kwargs):
        tenant_name = kwargs['tenant_name']
        user_name = kwargs['user_name']
        email = kwargs['email']
        password = kwargs['password']

        with TransactionTenantCreator(
                client=self.client, tenant_name=tenant_name) as tenant,\
                TransactionUserCreator(
                    client=self.client, user_name=user_name, password=password,
                    email=email, tenant_id=tenant.id) as user,\
                TransactionDefaultRoles(
                    client=self.client, user_id=user.id, tenant_id=tenant.id):
            if user.id is None:
                raise Exception("couldn't create keystone user")
            return (tenant.id, user.id)
