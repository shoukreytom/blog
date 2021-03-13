from django.urls import path

from .views import UsersListAPIView


urlpatterns = [
    path('', UsersListAPIView.as_view()),
]
