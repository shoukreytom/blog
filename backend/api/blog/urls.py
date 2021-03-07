from django.urls import path

from api.blog.views import (
    PostCreateListAPIView,
    PostRetrieveUpdateDeleteAPIView,
    CommentCreateListAPIView,
    CommentRetrieveUpdateDeleteAPIView,
    ReplyCreateListAPIView,
    ReplyRetrieveUpdateDeleteAPIView,
)


urlpatterns = [
    path("", PostCreateListAPIView.as_view()),
    path("<int:pk>/", PostRetrieveUpdateDeleteAPIView.as_view()),
    path("<int:post_pk>/comments/", CommentCreateListAPIView.as_view()),
    path(
        "<int:post_pk>/comments/<int:pk>/", CommentRetrieveUpdateDeleteAPIView.as_view()
    ),
    path(
        "<int:post_pk>/comments/<int:comment_pk>/replies/",
        ReplyCreateListAPIView.as_view(),
    ),
    path(
        "<int:post_pk>/comments/<int:comment_pk>/replies/<int:pk>/",
        ReplyRetrieveUpdateDeleteAPIView.as_view(),
    ),
]
