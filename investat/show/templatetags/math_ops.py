from django import template

register = template.Library()


def multiply(a, b):
    return round(a * b, 4)

def float_to_percent(a):
    return "{0:.4}%".format(a*100)

def round_by_k(a, b=4):
    return round(a, b)

def divide(a, b):
    if (b == 0):
        return 0
    return float(a) / b

register.filter('multiply', multiply)
register.filter('float_to_percent', float_to_percent)
register.filter('round', round_by_k)
register.filter('divide', divide)