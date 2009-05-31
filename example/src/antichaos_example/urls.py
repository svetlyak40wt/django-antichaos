from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from django_antichaos.utils import model_to_ctype
from antichaos_example.models import Link

admin.autodiscover()

urlpatterns = patterns('',
     (r'^$', 'django.views.generic.simple.redirect_to', {
            'url': '/antichaos/cloud/%d/' % model_to_ctype(Link).id
            }),
     (r'^admin/', include(admin.site.urls)),
     (r'^antichaos/', include('django_antichaos.urls')),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
)

