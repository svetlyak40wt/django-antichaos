from django.contrib.contenttypes.models import ContentType
from tagging.models import TaggedItem

__version__ = '0.1.0'

def get_tagged_models():
    cids = TaggedItem._default_manager.values('content_type').distinct()
    ctypes = ContentType._default_manager.filter(id__in = cids)
    return [ctype.model_class() for ctype in ctypes]
