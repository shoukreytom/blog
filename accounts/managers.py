from django.contrib.auth.models import BaseUserManager
from django.core.validators import ValidationError


class AccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValidationError("username is required")
        if not email:
            raise ValidationError("email is required")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username,
                                email=self.normalize_email(email),
                                password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
