from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
import base64

from .serializers import UserChangeSerializer, UserListSerializer, UserLoginSerializer, UserRegisterSerializer
from users.models import User


""" METHODS:
1- GET  ---> api/v1/users/ : returns list of users
2- POST ---> api/v1/users/ : register new user
"""


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRetrieveUpdateDeleteAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    serializer_class = UserChangeSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(request, email=email, password=password)
        data = {}
        if user:
            token = base64.b64encode(f"{email}:{password}".encode()).decode()
            data['Authorization'] = f"Basic {token}"
            status = 200
        else:
            data["detail"] = "authentication field."
            status = 400
        return Response(data, status=status)
