from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from .serializers import UsersSerializer, UserRegisterSerializer
from users.models import User


""" METHODS:
1- GET  ---> api/v1/users/ : returns list of users
2- POST ---> api/v1/users/ : register new user
"""


class UsersListAPIView(CreateAPIView, APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        serializer = UsersSerializer(qs, many=True)
        return Response(serializer.data)
