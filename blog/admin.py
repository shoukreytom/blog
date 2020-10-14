from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post


class PostAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('content', )
    fields = ('title', 'slug', 'content', 'status')
    list_display = ('title', 'content', 'status')
    list_filter = ('publish', 'update', 'status')
    search_fields = ('title', 'content')
    prepopulated_fields = {
        'slug': ('title', )
    }


admin.site.register(Post, PostAdmin)
