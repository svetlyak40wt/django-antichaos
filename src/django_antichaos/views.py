from pdb import set_trace

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django_antichaos.utils import process_commands
from tagging.models import Tag, TaggedItem


def cloud(request, ctype_id):
    admin_index = reverse('admin_index')

    if request.user.is_staff == False:
        return redirect(admin_index)

    ctype = ContentType._default_manager.get(id = ctype_id)

    if request.method == 'POST':
        changes = request.POST.getlist('changes')
        process_commands(ctype, changes)

    objects = Tag.objects.cloud_for_model(ctype.model_class())

    return render_to_response('antichaos/tag_cloud.html', dict(
        title = _('Tag cloud for %s') % _(ctype.model),
        ctype = ctype,
        objects = objects,
        root_path = admin_index,
    ), context_instance = RequestContext(request))


def preview(request, ctype_id, tag_id):
    ctype = ContentType._default_manager.get(id = ctype_id)

    tag = Tag.objects.get(id = tag_id)

    objects = TaggedItem.objects.get_by_model(
        ctype.model_class(), tag)

    limit = request.GET.get('limit', 5)
    total_count = objects.count()
    objects = objects[:limit]

    return render_to_response('antichaos/tag_preview.html', dict(
        tag = tag,
        ctype = ctype,
        objects = objects[:limit],
        more = total_count - len(objects),
    ), context_instance = RequestContext(request))

