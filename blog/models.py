from django.db import models
from django.utils import timezone


class Post(models.Model):
	title = models.CharField(max_length=50, blank=False, null=False)
	body = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
