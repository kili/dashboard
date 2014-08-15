from django.conf import settings


class BalanceLimits(object):

    @staticmethod
    def passed_limit(before, after):
        for limit in settings.BALANCE_LIMITS:
            if before >= limit and after < limit:
                return {'passed': True, 'limit': limit}
        return {'passed': False}
