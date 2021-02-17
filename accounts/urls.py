from django.urls import path, re_path

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('email/confirm/<str:token>/', views.confirm_email, name='confirm-email'),
]