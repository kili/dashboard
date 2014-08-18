import locale
from django.contrib.humanize.templatetags.humanize import intcomma


def format_currency(amount):
    amount = round(float(amount), 2)
    loc = locale.getlocale()
    locale.setlocale(locale.LC_ALL, '')
    formatted = locale.currency(amount)
    locale.setlocale(locale.LC_ALL, loc)
    return formatted
