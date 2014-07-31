from django.contrib.humanize.templatetags.humanize import intcomma

def format_currency(amount):
    dollars = round(float(amount), 2)
    return "$%s%s" % (intcomma(int(amount)), ("%0.2f" % amount)[-3:])
