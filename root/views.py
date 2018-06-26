from django.shortcuts import render_to_response
from django.template import RequestContext
 
 
def e_handler404(request):
    context = RequestContext(request)
    response = render_to_response('404.html', context.flatten(0))
    response.status_code = 404
    return response
