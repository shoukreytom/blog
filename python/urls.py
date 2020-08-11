from django.urls import path

from . import views


app_name = "python"


urlpatterns = [
	path('', views.introduction, name="introduction")
]
