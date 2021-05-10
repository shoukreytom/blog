from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms.models import BaseModelForm, ModelForm

from .models import (
    User, EmailAddress, EmailConfirmation, PasswordReset, 
    Profile, FollowNotification, VoteNotification
)
from .forms import UserRegisterationForm, UserChangeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserRegisterationForm
    form = UserChangeForm
    list_display = [
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    list_filter = [
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    search_fields = ["username", "email"]
    list_display_links = ["username", "email"]
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = [
        "user",
    ]


@admin.register(FollowNotification)
class FollowNotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'fromuser', 'touser', 'status']
    list_filter = [
        "fromuser", "touser", "status"
    ]

@admin.register(VoteNotification)
class VoteNotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'fromuser', 'touser', 'status']
    list_filter = [
        "fromuser", "touser", "status"
    ]


@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ["email", "user", "primary", "verified"]


@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ["email", "key", "created", "sent"]


admin.site.register(PasswordReset)
