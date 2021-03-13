from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegisterationForm(UserCreationForm):


    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]


class UserChangeForm(UserChangeForm):


    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]
