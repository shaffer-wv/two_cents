from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Post(models.Model):
	body = models.CharField(max_length=140)
	pub_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)

	class Meta:
		ordering = ["-pub_date"]

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by')

	def __unicode__(self):
		return self.user.username

# make sure a userprofile is created/saved with each user
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
