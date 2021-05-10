from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import secrets

from .managers import Published, Drafted
from .utils import upload_cover_photo_to, STATUS_CHOICES


class Post(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=250)
    slug        = models.SlugField(max_length=250, blank=True, null=True)
    content     = models.TextField()
    cover_photo = models.ImageField(upload_to=upload_cover_photo_to, 
                                    verbose_name="Cover Photo", 
                                    blank=True, null=True)
    upvotes       = models.PositiveBigIntegerField(default=0)
    downvotes     = models.PositiveBigIntegerField(default=0)
    status      = models.CharField(choices=STATUS_CHOICES, max_length=15, default='draft')
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = Published()
    drafted = Drafted()

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name="comments")
    post    = models.ForeignKey('Post', on_delete=models.CASCADE, 
                                related_name="comments")
    text    = models.TextField(max_length=500)
    upvotes       = models.PositiveBigIntegerField(default=0)
    downvotes     = models.PositiveBigIntegerField(default=0)
    status  = models.CharField(choices=STATUS_CHOICES, max_length=15, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = Published()
    drafted = Drafted()

    def __str__(self):
        return f"{self.text[:50]}"


class Reply(models.Model):
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name="replies")
    comment    = models.ForeignKey('Comment', on_delete=models.CASCADE, 
                                related_name="replies")
    text    = models.TextField(max_length=500)
    upvotes       = models.PositiveBigIntegerField(default=0)
    downvotes     = models.PositiveBigIntegerField(default=0)
    status  = models.CharField(choices=STATUS_CHOICES, max_length=15, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = Published()
    drafted = Drafted()

    
    class Meta:
        verbose_name_plural = "Replies"
    

    def __str__(self):
        return f"{self.text[:50]}"


@receiver(post_save, sender=Post)
def add_slug_field(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.title)+secrets.token_hex(5)
        instance.save()
