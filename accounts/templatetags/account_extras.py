from django import template
import random

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string into a list using the delimiter"""
    return value.split(delimiter)

@register.filter
def random(value):
    """Return a random item from a list"""
    return random.choice(value) 