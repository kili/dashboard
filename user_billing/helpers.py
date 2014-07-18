import decimal
from django.contrib.humanize.templatetags import humanize


class FormattingHelpers(object):

    @staticmethod
    def price(price):
        return u'${0}'.format(
            humanize.intcomma(
                decimal.Decimal(price).quantize(
                    decimal.Decimal('0.00'))))

    @staticmethod
    def hours(time):
        return u'{0}'.format(
            time.quantize(
                decimal.Decimal('0.00'),
                rounding=decimal.ROUND_UP))
