from django.db.models import fields
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError

from users.models import Profile, User
from .utils import JWT_PAYLOAD_HANDLER, JWT_ENCODE_HANDLER


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_active",
            "is_staff",
            "is_admin",
            "date_joined",
            "last_login",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def validate_username(self, value):
        reserved_list = ["auth", "register", "login", "accounts"]
        if len(value.split(" ")) > 1 and value not in reserved_list:
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
                    return user
            except IntegrityError:
                raise serializers.ValidationError("username or email is already exist")

        return serializers.ValidationError("username and email are required.")


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        max_length=128, write_only=True, style={"input_type": "password"}
    )
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password is not found."
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )
        return {"email": user.email, "token": jwt_token}


class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class ProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=500, required=False)
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "avatar",
            "title",
            "bio",
            "location",
            "followers",
            "following"
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserListSerializer(instance.user).data
        return data
    
    def get_followers(self, obj):
        return obj.followers.count()
    
    def get_following(self, obj):
        return obj.following.count()
