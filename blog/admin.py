from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment, Reply


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'status')
    list_filter = ('publish', 'update', 'status')
    search_fields = ('title', 'content')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('author', 'post', 'created', 'updated')
    search_fields = ('text', )


class ReplyAdmin(admin.ModelAdmin):
    list_filter = ('author', 'comment', 'created', 'updated')
    search_fields = ('text', )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
