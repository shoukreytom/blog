from django.urls import path, re_path

from . import views


urlpatterns = [
    re_path(r'^404', views.handler404),
    path('', views.PostsList.as_view(), name="blog-home"),
    path('post/new/', views.CreatePost.as_view(), name="create-post"),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name="post-detail"),
    path('post/<slug:slug>/update/', views.UpdatePost.as_view(), name="update-post"),
    path('post/<slug:slug>/delete/', views.DeletePost.as_view(), name="delete-post"),
    path('about/', views.about, name="about"),
    path('contact/', views.ContactView.as_view(), name="contact")
]
