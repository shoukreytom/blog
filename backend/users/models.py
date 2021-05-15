from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .managers import UserManager
from .utils import upload_avatar_to, NOTIFICATION_TYPES, NOTIFICATION_STATUS


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="last login")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class EmailAddress(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='email_addresses')
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    email = models.ForeignKey('EmailAddress', on_delete=models.CASCADE)
    key = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email.email


class PasswordReset(models.Model):
    email = models.EmailField(unique=True)
    enc_email = models.CharField(verbose_name='Encrypted Email', max_length=500, unique=True)
    token = models.CharField(max_length=500)


    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=upload_avatar_to, default='avatars/default.jpg')
    title = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=60, blank=True)
    followers = models.ManyToManyField('User', related_name='followers', blank=True)
    following = models.ManyToManyField('User', related_name='following', blank=True)

    def __str__(self):
        return f"<Profile <User {self.user.username}>>"


class NotificationBase(models.Model):
    fromuser = models.ForeignKey('User', on_delete=models.CASCADE, related_name="from user+")
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True


class FollowNotification(NotificationBase):

    def __str__(self):
        return f"<Notification from: {self.fromuser.username}>"


class VoteNotification(NotificationBase):
    voted_post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="voted post+")

    def __str__(self):
        return f"<Notification from: {self.fromuser.username}>"


class Notification(models.Model):
    TYPES_LIMIT = models.Q(app_label="users", model="follownotification") | models.Q(app_label="users", model="votenotification")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="notifications")
    follow_notification = models.ForeignKey(FollowNotification, blank=True, null=True, on_delete=models.SET_NULL)
    vote_notification = models.ForeignKey(VoteNotification, blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(
                        ContentType, 
                        on_delete=models.CASCADE,
                        limit_choices_to=TYPES_LIMIT
                    )
    content = GenericForeignKey('content_type', 'id')
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='unread')


    def clean(self, *args, **kwargs):
        if not self.follow_notification and not self.vote_notification:
            raise ValidationError("follow notification or vote notification is required.")
        if self.follow_notification and self.vote_notification:
            raise ValidationError("you can't have more than one type in one notification message.")
        if (self.content_type.model == "follownotification" and not self.follow_notification or 
            self.content_type.model == "votenotification" and not self.vote_notification):
            raise ValidationError("you should select the appropiate type for this notification.")
