from django.urls import path, re_path

from . import views


urlpatterns = [
	re_path(r'^404', views.handler404),
	path('', views.PostsList.as_view(), name="blog-home"),
	path('post/<int:pk>/', views.PostDetail.as_view(), name="post-detail"),
	path('about/', views.about, name="about"),
	path('contact/', views.contact, name="contact")
]
