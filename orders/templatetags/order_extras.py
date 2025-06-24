from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add the value and the argument"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0 