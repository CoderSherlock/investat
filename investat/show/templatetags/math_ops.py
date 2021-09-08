from django import template

register = template.Library()


def multiply(a, b):
    return round(a * b, 4)


register.filter('multiply', multiply)
