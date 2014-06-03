from django.conf.urls import patterns, url
from microblog import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='user_login'),
	url(r'^logout/$', views.user_logout, name='user_logout'),
	url(r'^add_post/$', views.add_post, name='add_post'),
	url(r'^profile/(?P<username>\w+)$', views.user_profile, name='user_profile'),
	url(r'^follow/(?P<username>\w+)$', views.follow, name='follow'),
	)