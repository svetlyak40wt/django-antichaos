from django.contrib.contenttypes.models import ContentType
from tagging.models import TaggedItem

def get_tagged_models():
    cids = TaggedItem._default_manager.values('content_type').distinct()
    ctypes = ContentType._default_manager.filter(id__in = cids)
    return [(ctype.id, ctype.model_class()) for ctype in ctypes]

def ctypeid_to_model_name(ctype_id):
    ctype = ContentType._default_manager.get(id = ctype_id)
    return '%s.%s' % (ctype.app_label, ctype.model)

