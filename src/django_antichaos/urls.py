from django.conf.urls.defaults import *

urlpatterns = patterns('django_antichaos.views',
    (r'^cloud/(?P<ctype_id>\d+)/$', 'cloud', {}, 'tag-cloud'),
)

