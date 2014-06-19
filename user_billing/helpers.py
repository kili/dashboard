import decimal
from django.contrib.humanize.templatetags import humanize


class FormattingHelpers(object):

    @staticmethod
    def price(price):
        price = decimal.Decimal(price).quantize(
            decimal.Decimal('0.00'))
        return u'${0}'.format(humanize.intcomma(price))

    @staticmethod
    def hours(time):
        hours = time.quantize(
            decimal.Decimal('0.00'),
            rounding=decimal.ROUND_UP)
        return u'{0}'.format(hours)
