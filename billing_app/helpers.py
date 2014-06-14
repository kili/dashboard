import decimal


class FormattingHelpers(object):

    @staticmethod
    def price(price):
        price = decimal.Decimal(price).quantize(
            decimal.Decimal('0.00'))
        return "${0}".format(price)

    @staticmethod
    def hours(time):
        hours = time.quantize(
            decimal.Decimal('0'),
            rounding=decimal.ROUND_DOWN)
        mins = ((time - hours) * 60).quantize(
            decimal.Decimal('0'))
        return "{0}:{1:02}".format(hours, mins)
