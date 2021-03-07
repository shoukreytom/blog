from django.urls import path, include


urlpatterns = [
    path('posts/', include("api.blog.urls")),
    path('users/', include("api.users.urls")),
]
