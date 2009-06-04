from pdb import set_trace

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, TemplateDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django_antichaos.utils import process_commands
from tagging.models import Tag, TaggedItem

def template_list(model, template_name):
    app_label = model._meta.app_label
    module_name = model._meta.module_name
    _locals = locals()
    return [
        'antichaos/%(app_label)s/%(module_name)s/%(template_name)s.html' % _locals,
        'antichaos/%(app_label)s/%(template_name)s.html' % _locals,
        'antichaos/%(template_name)s.html' % _locals,
    ]

def cloud(request, ctype_id):
    admin_index = reverse('admin_index')

    if request.user.is_staff == False:
        return redirect(admin_index)

    ctype = ContentType._default_manager.get(id = ctype_id)

    if request.method == 'POST':
        changes = request.POST.getlist('changes')
        process_commands(ctype, changes)

    model = ctype.model_class()
    objects = Tag.objects.cloud_for_model(model)

    return render_to_response(
        template_list(model, 'tag_cloud'),
        dict(
            title = _('Tag cloud for %s') % _(ctype.model),
            ctype = ctype,
            objects = objects,
            root_path = admin_index,
        ), context_instance = RequestContext(request))


def preview(request, ctype_id, tag_id):
    ctype = ContentType._default_manager.get(id = ctype_id)

    tag = Tag.objects.get(id = tag_id)

    skip = int(request.GET.get('skip', 0))
    top = int(request.GET.get('top', 5))
    next_skip = skip + top

    model = ctype.model_class()
    objects = TaggedItem.objects.get_by_model(model, tag)

    app_label = model._meta.app_label
    module_name = model._meta.module_name

    return render_to_response(
        template_list(model, 'tag_preview'),
        dict(
            tag = tag,
            ctype = ctype,
            objects = objects[skip:next_skip],
            skip = next_skip,
            top = top,
            more = len(objects[next_skip:]),
        ), context_instance = RequestContext(request))

