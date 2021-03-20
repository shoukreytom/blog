from hashlib import sha256
import secrets


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

def generate_key(email):
    enc_email = sha256(email.encode()).digest().hex()
    rand_txt = secrets.token_hex(15)
    key = enc_email + rand_txt
    if len(key) > 250:
        return key[:250]
    return key
