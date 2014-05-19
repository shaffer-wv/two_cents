from django.shortcuts import render, render_to_response
from django.template import RequestContext
from microblog.models import Post

# this will eventually go away
def index(request):
	context = RequestContext(request)

	posts = Post.objects.all()
	context_dict = {'posts': posts}

	return render_to_response('microblog/index.html', context_dict)
