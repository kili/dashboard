from keystoneclient.v3.roles import RoleManager
from keystoneclient.v3.client import Client
from django.conf import settings


class TransactionDefaultRoles():

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.user_id = kwargs['user_id']
        self.tenant_id = kwargs['tenant_id']

    def __enter__(self):
        self.assign_roles()

    def __exit__(self, type, value, traceback):
        pass

    def assign_roles(self):
        for role in self.get_role_ids():
            self.client.roles.add_user_role(self.user_id,
                                            role, tenant=self.tenant_id)

    def get_role_ids(self):
        return [
            role.id for role in self.client.roles.list()
            if role.name in settings.DEFAULT_ROLES]
