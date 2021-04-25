from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import (
    ProfileSerializer,
    UserChangeSerializer,
    UserListSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from hashlib import sha256
import secrets
from .permissions import IsOwnerOrAdmin, Isverified
from .utils import SendMessage
from users.models import EmailAddress, EmailConfirmation, Profile, User, PasswordReset


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
        response = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            response["account"] = {
                "status": "created",
                "message": "Your account has been created successfully."
            }
            email = request.data.get("email")
            email_addr = account.email_addresses.get(email=email)
            email_conf = EmailConfirmation.objects.get(email=email_addr)
            sm_obj = SendMessage()
            email_sent = sm_obj.send_confirmation_message(email, email_conf.key)
            if email_sent:
                email_conf.sent = timezone.now()
                email_conf.save()
                response["email"] = {
                    "status": "sent",
                    "message": "We have sent you an email with a link to confirm your email."
                }
            else:
                response["email"] = {
                    "status": "failed",
                    "message": "We couldn't send you an email, please try again later."
                }
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_400_BAD_REQUEST
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def confirm_email(request, token):
    response = {}
    try:
        email_conf = EmailConfirmation.objects.get(key=token)
        if str(email_conf) == str(request.user):
            email_addr = EmailAddress.objects.get(email=str(email_conf))
            email_addr.verified = True
            email_addr.save()
            email_conf.delete()
            response["message"] = "Your email has been confirmed successfully."
            status_code = status.HTTP_202_ACCEPTED
        else:
            raise Exception()
    except:
        response["message"] = "Email confirmation failed."
        status_code = status.HTTP_403_FORBIDDEN
    return Response(response, status=status_code)


"""METHODS:
    1- POST --> api/v1/users/follow/ 
        - adds a user to authenticated user's following list.
        - adds an authenticated user to a followed user's followers list.
    2- DELETE --> api/v1/users/follow/
        - removes a user from authenticated user's following list.
        - removes authenticate user from unfollowed users's followers list.
"""
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, username):
        data = {}
        data["OK"] = False
        status_code = status.HTTP_201_CREATED
        user = get_object_or_404(User, username=username)
        auth_user = request.user
        if user == auth_user:
            data["detail"] = "You can't follow or unfollow yourself"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            try:
                auth_user.profile.following.get(username=user.username)
                data["detail"] = "You're already following this user"
                status_code = status.HTTP_400_BAD_REQUEST
            except:
                profile = get_object_or_404(Profile, user=user)
                profile.followers.add(request.user)
                request.user.profile.following.add(user)
                data["OK"] = True
                data["detail"] = f"{user}, is added to your following list successfully."
        return Response(data, status=status_code)

    def delete(self, request, username):
        data = {}
        data["OK"] = False
        status_code = status.HTTP_200_OK
        user = get_object_or_404(User, username=username)
        auth_user = request.user
        if user == auth_user:
            data["detail"] = "You can't follow or unfollow yourself"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            try: 
                auth_user.profile.following.get(username=user.username)
                profile = get_object_or_404(Profile, user=user)
                profile.followers.remove(request.user)
                request.user.profile.following.remove(user)
                data["OK"] = True
                data["detail"] = f"{user}, is removed from your following list successfully."
            except ObjectDoesNotExist:
                data["detail"] = "You're not following this user"
                status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class FollowersListAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = user.profile.followers.all()
        serializer = UserListSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingListAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = user.profile.following.all()
        serializer = UserListSerializer(following, many=True)
        return Response(serializer.data)


class UserProfileAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            data = {"detail": "You've no permissions to edit this profile."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: let client provide url to redirect_url* with the key
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    data = {}
    email = request.POST.get('email')
    get_object_or_404(User, email=email)
    # TODO: generate token, save email and token to db
    token = secrets.token_hex(20)
    # TODO: encrypt email and append token :token to it
    enc_email = sha256(email.encode()).digest().hex()
    # TODO: send an email to the user with that url
    key = f'{enc_email}:{token}'
    sm_obj = SendMessage()
    msg_sent = sm_obj.send_passwordreset_message(email, key)
    if msg_sent:
        psw_reset, created = PasswordReset.objects.get_or_create(email=email)
        psw_reset.enc_email = enc_email
        psw_reset.token = token
        psw_reset.save()
        data['message'] = "we've sent a message to that email with a confirmation code."
        data['OK'] = True
    else:
        data['message'] = "sorry! something went wrong."
        data['OK'] = False
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, token=None):
    data = {}
    status_code = status.HTTP_200_OK
    email, token = token.split(':')
    psw_reset = get_object_or_404(PasswordReset, enc_email=email)
    if psw_reset.token == token:
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if (password1 and password2) and (password1 == password2):
                user = get_object_or_404(User, email=psw_reset.email)
                user.set_password(password2)
                user.save()
                # psw_reset.delete() TODO: uncomment this line for saving resources
                data['message'] = 'password is reset successfully.'
                data['OK'] = True
                status_code = status.HTTP_202_ACCEPTED
            else:
                data['message'] = 'password did not match.'
                data['OK'] = False
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            data['message'] = 'this request is verified, please set new password.'
            data['OK'] = True
    else:
        data['message'] = 'the provided token is unknown.'
        data['OK'] = False
        status_code = status_code.HTTP_403_FORBIDDEN
    return Response(data, status=status_code)
