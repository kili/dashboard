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

    @staticmethod
    def verify_input_date(option, opt, value, parser):
        try:
            setattr(parser.values,
                    option.dest,
                    parse(value,
                          yearfirst=True).replace(
                              tzinfo=timezone.get_default_timezone()))
        except Exception:
            raise OptionValueError('invalid date format, must be yyyy-mm-dd')
        if (getattr(parser.values,
                    option.dest) >= timezone.now().replace(hour=0,
                                                           minute=0,
                                                           second=0,
                                                           microsecond=0)):
            raise OptionValueError('date must be in the past')
