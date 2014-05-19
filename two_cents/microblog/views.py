from django.shortcuts import render, render_to_response
from django.template import RequestContext

# this will eventually go away
def index(request):
	context = RequestContext(request)
	return render_to_response('microblog/index.html')
