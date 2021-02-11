from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings

from .managers import AccountManager


class Account(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = AccountManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_labbel):
        return True


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, default=settings.AUTH_USER_MODEL, related_name='profile')
    image = models.ImageField(upload_to='profile-pics/', default='default.jpg')

    def __str__(self):
        return "<Profile <{0}>>".format(self.user.username)
