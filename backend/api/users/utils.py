from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework_jwt.settings import api_settings

import os


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class SendMessage:

    def __init__(self):
        if os.path.exists(os.path.join(settings.BASE_DIR / "config", "hidden.py")):
            self.__host = "localhost"
            self.__url = f"http://{self.__host}:8000/api/v1/users/auth/email/confirm"
            self.__pwdurl = f"http://{self.__host}:8000/api/v1/users/auth/password/reset/confirm"
        else:
            self.__host = "djangoblogdemo.herokuapp.com"
            self.__url = f"https://{self.__host}/api/v1/users/auth/email/confirm"
            self.__pwdurl = f"https://{self.__host}/api/v1/users/auth/password/reset/confirm"

        self.__EMAIL_CONFIRMATION_MSG = """<strong>Hello from {host}!</strong><br>
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
        self.__PASSWORD_RESET_MSG = """<strong>Hello from {host}!</strong><br>
        <p>You're receiving this e-mail because someone has requested a password reset with this e-mail on {host}.<br>
        To confirm the request, please click the below button<p><br>
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

    def send_confirmation_message(self, email, key):
        message = self.__EMAIL_CONFIRMATION_MSG.format(host=self.__host, url=self.__url, key=key)
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

    def send_passwordreset_message(self, email, key):
        message = self.__PASSWORD_RESET_MSG.format(host=self.__host, url=self.__pwdurl, key=key)
        msg = EmailMessage(
            "Password Reset",
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
