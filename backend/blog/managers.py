from django.db.models import Manager


class Published(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Drafted(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')
