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


def process_merge(ctype, tag_left, tag_right):
    logger = logging.getLogger('antichaos.utils')

    tag_left = Tag.objects.get(id=tag_left)
    tag_right = Tag.objects.get(id=tag_right)

    logger.debug('merging tag "%s" to tag "%s"' % (tag_right.name, tag_left.name))

    delete_params = {}
    if hasattr(settings, 'MULTILINGUAL_TAGS') is True:
        """Specialization for tagging-ng's delete method."""
        delete_params['update'] = False

    for item in tag_right.items.filter(content_type = ctype):
        if tag_left.items.filter(
                content_type = ctype,
                object_id = item.object_id).count() != 0:
            logger.debug('item "%s" already binded to tag "%s"' % (item, tag_left))
            item.delete(**delete_params)
        else:
            item.tag = tag_left
            item.save()
            logger.debug('item "%s" merged' % item)

        update_objects_tags(item.object)

def process_rename(ctype, old_tag_id, new_name):
    logger = logging.getLogger('antichaos.utils')

    new_tag, created = Tag.objects.get_or_create(name = new_name)
    if created:
        logger.debug('tag "%s" was created' % new_name)

    process_merge(ctype, new_tag.id, old_tag_id)


def process_commands(ctype, commands):
    logger = logging.getLogger('antichaos.utils')
    logger.debug('processing commands')

    processors = dict((name.split('_', 1)[1], value)
        for name, value in globals().iteritems()
            if name.startswith('process_') and name != 'process_commands')

    for cmd in commands:
        cmd, args = cmd.split('|', 1)
        proc = processors.get(cmd, None)
        if proc is not None:
            proc(ctype, *args.split('|'))

