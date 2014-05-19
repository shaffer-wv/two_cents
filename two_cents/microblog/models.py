from django.db import models

# Create your models here.
class Post(models.Model):
	body = models.CharField(max_length=140)
	pub_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-pub_date"]