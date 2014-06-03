from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from microblog.models import Post
from microblog.forms import UserForm, LoginForm, PostForm
import utilities

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
		form = LoginForm()
	return render_to_response('microblog/login.html', {'login_form': form,}, context)


@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/login/')


@login_required
def index(request):
	context = RequestContext(request)

	current_user = request.user

	# get users that logged in user is following
	following = current_user.userprofile.follows.all()

	# get the posts from following users
	posts = []
	for person in following:
		x = Post.objects.filter(author = person.user)
		for post in x:
			posts.append(post)

	# sort the post in order of pub_date
	posts = sorted(posts, key=lambda post: post.pub_date, reverse=True)


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

	posts = Post.objects.filter(author=target_user)

	context_dict = {'target_user': target_user}
	context_dict['own_profile'] = own_profile
	context_dict['posts'] = posts


	return render_to_response('microblog/profile.html', context_dict, context)

@login_required
def follow(request, username):
	user_to_follow = User.objects.get(username=username)

	# not sure if I need these first 2 if statements
	if user_to_follow == None:
		# User not found
		# Eventually need to enable messages
		return HttpResponseRedirect('/')

	if user_to_follow == request.user:
		# Already following yourself
		return HttpResponseRedirect('/')

	user = request.user
	user.userprofile.follows.add(user_to_follow.userprofile)
	user.save()

	return HttpResponseRedirect('/')

@login_required
def search(request):
	context = RequestContext(request)
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

		entry_query = get_query(query_string, ['body'])

		found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

	return render_to_response('search/search_results.html', { 'query_string': query_string, 'found_entries': found_entries },
		context)

@login_required
def followers(request):
	context = RequestContext(request)

	user = request.user

	followers_list = user.userprofile.followed_by.all()
	# dont want to display own profile in followers list
	followers_list = followers_list[1:]

	return render_to_response('microblog/followers.html', { 'followers_list': followers_list }, context)

@login_required
def following(request):
	context = RequestContext(request)

	user = request.user

	following_list = user.userprofile.follows.all()
	# dont want to display own profile in followers list
	following_list = following_list[1:]

	return render_to_response('microblog/following.html', { 'following_list': following_list }, context)
