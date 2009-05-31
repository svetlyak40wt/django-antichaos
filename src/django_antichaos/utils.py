import logging

from django.contrib.contenttypes.models import ContentType
from tagging.models import TaggedItem

def get_tagged_models():
    cids = TaggedItem._default_manager.values('content_type').distinct()
    ctypes = ContentType._default_manager.filter(id__in = cids)
    return [(ctype.id, ctype.model_class()) for ctype in ctypes]


def model_to_ctype(model):
    return ContentType._default_manager.get_for_model(model)

def process_merge(ctype, tag_left, tag_right):
    logger = logging.getLogger('antichaos.utils')
    logger.debug('merging tag_id %s to tag_id %s' % (tag_right, tag_left))

def process_commands(ctype, commands):
    logger = logging.getLogger('antichaos.utils')
    logger.debug('processing commands')

    processors = dict((name.split('_', 1)[1], value)
        for name, value in globals().iteritems()
            if name.startswith('process_') and name != 'process_commands')

    for cmd in commands:
        cmd, args = cmd.split(' ', 1)
        proc = processors.get(cmd, None)
        if proc is not None:
            proc(ctype, *args.split(' '))

