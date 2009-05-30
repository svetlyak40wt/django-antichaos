from django import template

from django_antichaos.utils import get_tagged_models

register = template.Library()

@register.inclusion_tag('antichaos/tagged_models.html')
def tagged_models():
    models = [dict(name = m.__name__, model = m, ctype_id = ctype_id)
                   for ctype_id, m in get_tagged_models()]
    return dict(models = models)
