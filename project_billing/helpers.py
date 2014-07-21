import decimal
from dateutil.parser import parse
from optparse import OptionValueError
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone


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

    @classmethod
    def verify_date_format(cls, option, opt, value, parser):
        try:
            cls.get_datetime(value)
        except Exception:
            raise OptionValueError('invalid date format, must be yyyy-mm-dd')
        setattr(parser.values, option.dest, value)

    @staticmethod
    def get_datetime(string):
        return parse(string, yearfirst=True).replace(
            tzinfo=timezone.get_default_timezone())
