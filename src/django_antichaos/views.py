from django.shortcuts import render_to_response
from django.template import RequestContext

def cloud(request, ctype = None):
    return render_to_response('antichaos/tag-cloud.html', dict(
        objects = ['blah'],
    ), context_instance = RequestContext(request))
