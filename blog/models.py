from django.conf import settings
from django.db import models
from autoslug import AutoSlugField
from accounts.models import Account


class PublishedManager(models.Manager):
    def get_queryset(self):
        return Post.objects.filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
    ]
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique_with='publish__month')
    content = models.TextField()
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, default=settings.AUTH_USER_MODEL)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(
        auto_now_add=True, verbose_name='published date')
    update = models.DateTimeField(auto_now=True, verbose_name='updated date')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(Account, on_delete=models.CASCADE,
                               default=settings.AUTH_USER_MODEL, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:30]}..."


class Reply(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, default=settings.AUTH_USER_MODEL)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f"{self.text[:30]}..."
