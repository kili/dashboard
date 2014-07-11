from accounting.managers import AccountManager


def balance(request):
    return {'balance':
        AccountManager().get_user_account(
            request.user.tenant_id).balance()}
