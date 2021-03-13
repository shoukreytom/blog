from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UsersSerializer, UserRegisterSerializer, UserLoginSerializer
from users.models import User

class UserLoginView(RetrieveAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserRegisterView(CreateAPIView):

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

""" METHODS:
1- GET  ---> api/v1/users/ : returns list of users
2- POST ---> api/v1/users/signup : register new user
3- GET ---> api/v1/users/signin : login user
"""


class UsersListAPIView(CreateAPIView, APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        serializer = UsersSerializer(qs, many=True)
        return Response(serializer.data)
