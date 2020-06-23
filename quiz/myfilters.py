from django import template

register = template.Library()


@register.filter(name="level_filter")
def level_filter(value):
    result = ""

    return result
