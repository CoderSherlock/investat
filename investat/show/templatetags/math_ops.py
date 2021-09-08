from django import template

register = template.Library()


def multiply(a, b):
    return a * b


register.filter('multiply', multiply)
