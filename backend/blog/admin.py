from django.contrib import admin

from .models import Post, Comment, Reply


class InlineReply(admin.TabularInline):
    model = Reply
    extra = 1


class InlineComment(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['slug', 'title', 'author', 'status']
    list_filter = ['status', 'created', 'updated']
    list_display_links = ['slug', 'title']
    inlines = [InlineComment]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post', 'author']
    list_filter = ['author', 'post', 'created', 'updated']
    inlines = [InlineReply]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'comment', 'author']
    list_filter = ['author', 'comment', 'created', 'updated']
