from django.core.management.base import BaseCommand
from django.conf import settings

import os
import json
import datetime
from blog.models import Post


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, "data.json"), "r") as json_file:
            data = json.load(json_file)
            for pk in data:
                raw = data[pk]
                title = raw['title']
                summary = raw['summary']
                body = raw['body']
                date = raw['date_posted']

                # parsing date
                date, time = date.split()
                date = date.split("/")
                time = time.split(":")

                date_posted = datetime.datetime(
                    day=int(date[0]), month=int(date[1]), year=int(date[2]), hour=int(time[0]), minute=int(time[1]))
                try:
                    Post.objects.get(title=title, summary=summary)
                    print(f"{title}, is already exist!!!")
                except Post.DoesNotExist:
                    post = Post(title=title, summary=summary,
                                body=body, date_posted=date_posted)
                    post.save()
