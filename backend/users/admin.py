from django.contrib import admin

from .models import User, Profile, Notifications



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'is_verified', 'last_login', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_admin', 'is_verified', 'is_superuser', 'last_login', 'date_joined']
    search_fields = ['username', 'email']
    list_display_links = ['username', 'email']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['user', ]


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_filter = ['user', ]
