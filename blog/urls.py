from django.urls import path, re_path
from django.conf.urls import url

from . import views


urlpatterns = [
	re_path(r"^$|blog/", views.PostsList.as_view(), name="blog-home"),
	path('post/<int:pk>/', views.PostDetail.as_view(), name="post-detail"),
	path('about/', views.about, name="about"),
	path('contact/', views.contact, name="contact")
]
