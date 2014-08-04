from django.contrib.humanize.templatetags.humanize import intcomma


def format_currency(amount):
    amount = round(float(amount), 2)
    return '${}{}'.format(intcomma(int(amount)), '{:0.2f}'.format(amount)[-3:])
