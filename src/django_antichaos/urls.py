from django.conf.urls.defaults import *

urlpatterns = patterns('django_antichaos.views',
    (r'^cloud/(?P<ctype>\d+)/$', 'cloud', {}, 'tag-cloud'),
)

