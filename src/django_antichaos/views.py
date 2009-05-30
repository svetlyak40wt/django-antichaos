from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType

from django_antichaos.utils import ctypeid_to_model_name
from tagging.models import Tag

def cloud(request, ctype_id):
    ctype = ContentType._default_manager.get(id = ctype_id)
    objects = Tag.objects.cloud_for_model(ctype.model_class())

    return render_to_response('antichaos/tag-cloud.html', dict(
        ctype = ctype,
        objects = objects,
    ), context_instance = RequestContext(request))
