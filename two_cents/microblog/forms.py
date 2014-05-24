from django.contrib.auth.models import User
from django import forms
from microblog.models import Post

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'password')

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'cols':100, 'rows':10}),
		}
