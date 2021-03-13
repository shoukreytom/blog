from django.urls import path

from .views import UsersListAPIView, UserRegisterView, UserLoginView


urlpatterns = [
    path('', UsersListAPIView.as_view()),
    path('signup/', UserRegisterView.as_view()),
    path('signin/', UserLoginView.as_view()),
]
