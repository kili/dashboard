from keystoneclient.v2_0.users import User


class TransactionUserCreator(User):

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.user_name = kwargs['user_name']
        self.password = kwargs['password']
        self.tenant_id = kwargs['tenant_id']

    def __enter__(self):
        self.user = self.client.users.create(
            self.user_name,
            self.password,
            tenant_id=self.tenant_id,
            enabled=False,
        )
        return self.user

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.client.users.delete(self.user.id)
