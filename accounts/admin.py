from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display=['username', 'email', 'date_joined',
        'last_login', 'is_active', 'is_admin', 'is_superuser']
    list_filter=['date_joined', 'last_login',
        'is_active', 'is_admin', 'is_superuser']
    search_fields = ['username', 'email']


admin.site.register(Account, AccountAdmin)
