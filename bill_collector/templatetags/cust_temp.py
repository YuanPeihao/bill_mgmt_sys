from django import template
register = template.Library()


@register.filter
def index(var, idx):
    return var[idx]