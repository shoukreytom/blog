from django.core.management.base import BaseCommand
from django.conf import settings

import json
import os
from blog.models import Post


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        posts_dic = dict()
        for post in posts:
            pk = post.pk
            title = post.title
            summary = post.summary
            body = post.body
            date = post.date_posted
            posts_dic[f'{pk}'] = {
                'title': title,
                'summary': summary,
                'body': body,
                'date_posted': f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"
            }
        with open(os.path.join(settings.BASE_DIR, "data.json"), "w") as out:
            json.dump(posts_dic, out)
