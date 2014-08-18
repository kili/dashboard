import re
from babel import numbers


def format_currency(orig_amount):
    amount = numbers.format_currency(
        abs(round(float(orig_amount), 2)), 'USD')
    if orig_amount < 0:
        pos = re.search("\d", amount)
        amount = amount[:pos.start()] + '-' + amount[pos.start():]
    return amount
