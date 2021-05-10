from django.urls import path

from .views import (
    FollowAPIView,
    FollowersListAPIView,
    FollowingListAPIView,
    UserListAPIView,
    UserProfileAPIView,
    UserRetrieveUpdateDeleteAPIView,
    UserRegisterAPIView,
    UserLoginAPIView, confirm_email,
    password_reset_request, password_reset_confirm,
    NotificationListAPIView
)


urlpatterns = [
    path("", UserListAPIView.as_view()),
    path("<str:username>/", UserRetrieveUpdateDeleteAPIView.as_view()),
    path("<str:username>/profile/", UserProfileAPIView.as_view()),
    path("<str:username>/follow/", FollowAPIView.as_view()),
    path("<str:username>/followers/", FollowersListAPIView.as_view()),
    path("<str:username>/following/", FollowingListAPIView.as_view()),
    path("<str:username>/notifactions/", NotificationListAPIView.as_view()),
    path("auth/register/", UserRegisterAPIView.as_view()),
    path("auth/login/", UserLoginAPIView.as_view()),
    path("auth/email/confirm/<str:token>/", confirm_email),
    path("auth/password/reset/", password_reset_request),
    path("auth/password/reset/confirm/<str:token>/", password_reset_confirm),
]
