from django.urls import path

from .views import UserLoginAPIView, UserRegisterAPIView, UserRetrieveUpdateDeleteAPIView, UserListAPIView


urlpatterns = [
    path("", UserListAPIView.as_view()),
    path("<str:username>/", UserRetrieveUpdateDeleteAPIView.as_view()),
    path("auth/register/", UserRegisterAPIView.as_view()),
    path("auth/login/", UserLoginAPIView.as_view()),
]
