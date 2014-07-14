from accounting.managers import AccountManager


def balance(request):
    if request.user.is_authenticated():
        return {'balance':
            AccountManager().get_user_account(
                request.user.tenant_id).balance()}
    return {}
