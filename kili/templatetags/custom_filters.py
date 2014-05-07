from django import template

register = template.Library()


@register.filter
def replace(value, args):
    """Removes all values of arg from the given string."""
    return value.replace(args.split(",")[0], args.split(",")[1])
