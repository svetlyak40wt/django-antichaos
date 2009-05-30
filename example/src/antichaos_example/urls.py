from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

front_dict = {
    'extra_context': {'title': _('Main page')},
    'template': 'antichaos_example/front_page.html',
}

urlpatterns = patterns('',
     (r'^$', 'django.views.generic.simple.direct_to_template', front_dict),
     (r'^admin/(.*)', admin.site.root, {}, 'admin-root'),
     (r'^antichaos/', include('django_antichaos.urls')),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
)

