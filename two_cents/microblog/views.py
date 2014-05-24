from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from microblog.models import Post
from microblog.forms import UserForm, LoginForm, PostForm

# user authentication views

def register(request):
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			# mark user as follower of themselves
			user.userprofile.follows.add(user.userprofile)
			user.save()

			registered = True
		else:
			print user_form.errors
	else:
		user_form = UserForm()

	return render_to_response('microblog/register.html', {'user_form': user_form, 'registered': registered}, context)


def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse("Your account is disabled.")
			else:
				print "Invalid login details: {0}, {1}".format(username, password)
				return HttpResponse("Invalid login details supplied.")
	else:
		form = LoginForm()
	return render_to_response('microblog/login.html', {'login_form': form,}, context)


@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/login/')


@login_required
def index(request):
	context = RequestContext(request)


	posts = Post.objects.all()
	context_dict = {'posts': posts}

	return render_to_response('microblog/index.html', context_dict, context)


@login_required
def add_post(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = PostForm()

	return render_to_response('microblog/add_post.html', {'form': form}, context)

@login_required
def user_profile(request, username):
	context = RequestContext(request)

	target_user = User.objects.get(username=username)
	if target_user == request.user:
		own_profile = True
	else:
		own_profile = False

	return render_to_response('microblog/profile.html', {'target_user': target_user, 'own_profile': own_profile,}, context)


