STATUS_CHOICES = [
    # first: Stored value, second: Displayed value
    ('draft', 'Draft'),
    ('published', 'Published'),
]
def upload_cover_photo_to(instance, filename):
    return f"post-photos/{instance.author.username}/{filename}"