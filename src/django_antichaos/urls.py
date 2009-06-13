import logging
import os.path

from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('django_antichaos.views',
    (r'^cloud/(?P<ctype_id>\d+)/$', 'cloud', {}, 'tag-cloud'),
    (r'^cloud/(?P<ctype_id>\d+)/preview/(?P<tag_id>\d+)/$', 'preview', {}, 'tag-preview'),
)

# create link in media directory
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)

APP_MEDIA_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    'antichaos')

_local = os.path.join(
            os.path.dirname(__file__),
            'media')

_logger = logging.getLogger('antichaos')

if os.path.islink(APP_MEDIA_ROOT):
    _real_path =os.path.realpath(APP_MEDIA_ROOT)
    if _real_path != _local:
        _logger.warning('removing old link %s' % _real_path)
        os.unlink(APP_MEDIA_ROOT)

if not os.path.exists(APP_MEDIA_ROOT):
    _logger.info('linking %r to %r' % (_local, APP_MEDIA_ROOT))
    os.symlink(_local, APP_MEDIA_ROOT)
