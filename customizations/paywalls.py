from accounting import managers
from horizon import exceptions
from horizon import messages


account_manager = managers.AccountManager()
acceptable_balance = 1


def filter_action(self, request, context):
    balance = account_manager.get_user_account(
        request.user.tenant_id).balance()
    if balance < acceptable_balance:
        messages.error(request,
            "You have insufficient funds to take this action."
            "You must transfer a minimum 30 USD to your account "
            "in order to take this action.")
        raise exceptions.Http302("/billing/")
        return False

    return self.do_handle(request, context)
