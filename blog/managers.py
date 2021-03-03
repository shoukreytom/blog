from django.db.models import Manager


class PublishedPosts(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class DraftedPosts(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')
