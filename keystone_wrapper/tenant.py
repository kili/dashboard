from keystoneclient.v2_0.tenants import Tenant, TenantManager


class TransactionTenantCreator(Tenant):

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.tenant_name = kwargs['tenant_name']

    def __enter__(self):
        self.tenant = self.client.tenants.create(self.tenant_name)
        return self.tenant

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.client.tenants.delete(self.tenant.id)
