from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }
    
    def validate_username(self, value):
        if len(value.split(" ")) > 1:
            raise serializers.ValidationError("Invalid username")
        return value.lower()


    def save(self):
        username = self.validated_data.get("username", None)
        email = self.validated_data.get("email", None)
        password = self.validated_data.get("password", None)
        password2 = self.validated_data.get("password2", None)

        if username and email:
            try:
                user = User.objects.create(username=username, email=email)
                if password == password2:
                    user.set_password(password2)
                    user.save()
            except IntegrityError:
                raise serializers.ValidationError("username or email is already exist")
        return serializers.ValidationError("username and email are required.")

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }