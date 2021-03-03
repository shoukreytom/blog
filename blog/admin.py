from django.contrib import admin

from .models import Post, Comment, Reply


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['slug', 'title', 'author', 'status']
    list_filter = ['status', 'created', 'updated']
    list_display_links = ['slug', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post', 'author']
    list_filter = ['author', 'post', 'created', 'updated']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'comment', 'author']
    list_filter = ['author', 'comment', 'created', 'updated']
