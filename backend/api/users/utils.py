from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework_jwt.settings import api_settings

import os


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def send_email(email, key):
    if os.path.exists(os.path.join(settings.BASE_DIR / "config", "hidden.py")):
        host = "localhost"
        url = f"http://{host}:8000/api/v1/users/auth/email/confirm"
    else:
        host = "djangoblogdemo.herokuapp.com"
        url = f"https://{host}/api/v1/users/email/confirm"

    message = f"""<strong>Hello from {host}!</strong><br>
<p>You're receiving this e-mail because your email address has been used e-mail to register an account on {host}.<br>
To confirm this is correct, click the below button<p><br>
<center>
    <form method="GET" action="{url}/{key}/">
        <button type="submit">Confirm Email</button>
    </form>
</center>
<br/>
<br>
<p>or copy this link: {url}/{key}/ and paste it into your browser.</p><br>
Thank you for using {host}!<br>
    """
    msg = EmailMessage(
        "Email Confirmation",
        message,
        settings.EMAIL_HOST_USER,
        [email, ]
    )
    msg.content_subtype = "html"
    try:
        msg.send(fail_silently=False)
        return True
    except:
        return False
