NOTIFICATION_TYPES = [
    ('follow', 'Follow'),
    ('comment', 'Comment'),
    ('reply', 'Reply'),
    ('vote', 'Vote'),
]
NOTIFICATION_STATUS = [
    ('read', 'Read'),
    ('unread', 'Unread'),
]

def upload_avatar_to(instance, filename):
    return f"avatars/{instance.user.username}/{filename}"
