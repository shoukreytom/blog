from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy


class PublishedManager(models.Manager):
    def get_queryset(self):
        return Post.objects.filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(
        auto_now_add=True, verbose_name='published date')
    update = models.DateTimeField(auto_now=True, verbose_name='updated date')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
