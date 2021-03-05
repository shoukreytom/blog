from django.contrib.auth import models


class UserManager(models.BaseUserManager):
    def create_user(self, username, email, password=None, *args, **kwargs):
        if not username:
            raise ValueError("Username is required.")
        if not email:
            raise ValueError("Email is required.")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        return user
    
    def create_superuser(self, username, email, password, *args, **kwargs):
        user = self.create_user(username=username, 
                        email=self.normalize_email(email), 
                        password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user
