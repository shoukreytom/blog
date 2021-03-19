from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserChangeSerializer,
    UserListSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from .permissions import IsOwnerOrAdmin, Isverified
from users.models import User


class UserLoginAPIView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "User logged in  successfully",
            "token": serializer.data["token"],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserRegisterAPIView(CreateAPIView):

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            "success": "True",
            "status code": status_code,
            "message": "User registered  successfully",
        }

        return Response(response, status=status_code)


""" METHODS:
1- GET  ---> api/v1/users/ : returns list of users
2- POST ---> api/v1/users/signup : register new user
3- GET ---> api/v1/users/signin : login user
"""


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)


class UserRetrieveUpdateDeleteAPIView(
    DestroyModelMixin, UpdateModelMixin, RetrieveAPIView
):
    serializer_class = UserChangeSerializer
    permission_classes = (Isverified, IsOwnerOrAdmin, )
    queryset = User.objects.all()
    lookup_field = "username"

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
