from django.urls import path

from blog.api.views import PostApiList, post_detail_view, PostDestroyApi


app_name = "blog"


urlpatterns = [
    path('', PostApiList.as_view()),
    path('posts/', PostApiList.as_view()),
    path('<int:pk>/', post_detail_view),
    path('<int:pk>/delete/', PostDestroyApi.as_view()),
]
