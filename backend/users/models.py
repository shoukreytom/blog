from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import UserManager
from .utils import upload_avatar_to, NOTIFICATION_TYPES, NOTIFICATION_STATUS


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="last login")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', related_name='followers')
    following = models.ManyToManyField('self', related_name='following')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=upload_avatar_to, default='avatars/default.jpg')

    def __str__(self):
        return f"<Profile <User {self.user.username}>>"


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    notif_type = models.CharField(verbose_name='Type', max_length=10, choices=NOTIFICATION_TYPES, default='follow')
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='unread')
    action_url = models.URLField(verbose_name='URL')

    def __str__(self):
        return f"<Notification <User {self.user.username}>>"


    class Meta:
        verbose_name_plural = 'Notifications'


@receiver(post_save, sender=User)
def save_profile(sender, instance=None, created=None, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
