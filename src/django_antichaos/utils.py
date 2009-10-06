import logging

from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
from tagging.utils import edit_string_for_tags
from tagging import settings

def get_tagged_models():
    cids = TaggedItem._default_manager.values('content_type').distinct()
    ctypes = ContentType._default_manager.filter(id__in = cids)
    return [(ctype.id, ctype.model_class()) for ctype in ctypes]


def model_to_ctype(model):
    return ContentType._default_manager.get_for_model(model)


def update_objects_tags(object):
    if object is None:
        return

    object_tags = Tag.objects.get_for_object(object)
    tags_as_string = edit_string_for_tags(object_tags)

    for field in object._meta.fields:
        if isinstance(field, TagField):
            setattr(object, field.attname, tags_as_string)
            object.save()
            break


def process_merge(ctype, to_tag, from_tag):
    logger = logging.getLogger('antichaos.utils')

    try:
        to_tag = Tag.objects.get(id=to_tag)
    except Tag.DoesNotExist:
        logger.error('skip merge from_tag=%(from_tag)s to_tag=%(to_tag)s cause to_tag is missing.' % locals())
        return

    try:
        from_tag = Tag.objects.get(id=from_tag)
    except Tag.DoesNotExist:
        logger.error('skip merge from_tag=%(from_tag)s to_tag=%(to_tag)s cause from_tag is missing.' % locals())
        return

    logger.debug('merging tag "%s" to tag "%s"' % (from_tag.name, to_tag.name))

    if hasattr(settings, 'MULTILINGUAL_TAGS'):
        """Specialization for tagging-ng's delete method."""
        from tagging.utils import merge
        merge(to_tag, from_tag, ctype)
        return

    for item in from_tag.items.filter(content_type = ctype):
        if to_tag.items.filter(
                content_type = ctype,
                object_id = item.object_id).count() != 0:
            logger.debug('item "%s" already binded to tag "%s"' % (item, to_tag))
            item.delete()
        else:
            item.tag = to_tag
            item.save()
            logger.debug('item "%s" merged' % item)

        update_objects_tags(item.object)


def process_rename(ctype, tag_id, new_value):
    logger = logging.getLogger('antichaos.utils')

    new_tag, created = Tag.objects.get_or_create(name = new_value)
    if created:
        logger.debug('tag "%s" was created' % new_value)

    process_merge(ctype, to_tag = new_tag.id, from_tag = tag_id)


def process_commands(ctype, commands, save_to = None):
    logger = logging.getLogger('antichaos.utils')
    logger.debug('processing commands')

    processors = dict((name.split('_', 1)[1], value)
        for name, value in globals().iteritems()
            if name.startswith('process_') and name != 'process_commands')

    if save_to != None:
        file = open(save_to, 'w')
        file.write('# model "%s.%s"\n' % (ctype.app_label, ctype.model))
        lines = list(cmd.strip(',').encode('utf-8') + '\n' for cmd in commands)
        file.writelines(lines)

    for cmd in commands:
        cmd = cmd.strip()
        if cmd.startswith('#'):
            continue

        kwargs = dict(
            (str(key), value) for key, value in (
                c.split('=') for c in cmd.split(',') if c))
        action = kwargs.pop('action')
        proc = processors.get(action, None)
        if proc is not None:
            proc(ctype, **kwargs)

