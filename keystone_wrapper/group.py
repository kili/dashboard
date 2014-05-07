from keystoneclient.v3 import groups


class TransactionGroupCreator(groups.Group):

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.group_name = kwargs['group_name']
        self.domain_id = kwargs['domain_id']

    def __enter__(self):
        self.group = self.client.groups.create(self.group_name,
                                               self.domain_id)
        return self.group

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.client.groups.delete(self.group.id)
