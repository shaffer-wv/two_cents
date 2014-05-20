from django.contrib import admin
from microblog.models import Post, UserProfile

# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
