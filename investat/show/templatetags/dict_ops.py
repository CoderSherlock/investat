from django import template

register = template.Library()


def get_item(dic, key):
    return dic.get(key)


register.filter('get_item', get_item)
