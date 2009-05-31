from urlparse import urljoin
from django import template
from django.conf import settings

from django_antichaos.utils import get_tagged_models

register = template.Library()

def tagged_models():
    models = [dict(name = m.__name__, model = m, ctype_id = ctype_id)
                   for ctype_id, m in get_tagged_models()]
    return dict(models = models)
tagged_models = register.inclusion_tag('antichaos/tag_cloud_list.html')(tagged_models)

def antichaos_media_prefix():
    return urljoin(settings.MEDIA_URL, 'antichaos/')
antichaos_media_prefix = register.simple_tag(antichaos_media_prefix)

