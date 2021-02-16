from django.contrib import admin

from .models import Account, Profile


class AccountAdmin(admin.ModelAdmin):
    list_display=['email', 'username', 'is_active',
        'is_superuser', 'is_verified', 'last_login', 'date_joined']
    list_filter=['date_joined', 'last_login',
        'is_active', 'is_admin', 'is_superuser', 'is_verified']
    search_fields = ['username', 'email']


admin.site.site_header = "Blog Admin"
admin.site.site_title = "Blog"

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
