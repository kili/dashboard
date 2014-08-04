from accounting import utils


def balance(request):
    if request.user.is_authenticated():
        return {'balance': utils.balance(request)}
    return {}
