from keystoneclient.v3.domains import Domain


class TransactionDomainCreator(Domain):

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.domain_name = kwargs['domain_name']

    def __enter__(self):
        self.domain = self.client.domains.create(self.domain_name)
        return self.domain

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.client.domains.update(self.domain.id, enabled=False)
            self.client.domains.delete(self.domain.id)

