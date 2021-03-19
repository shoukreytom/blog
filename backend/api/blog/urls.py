from django.urls import path

from api.blog.views import (
    PostCreateListAPIView,
    PostRetrieveUpdateDeleteAPIView,
    CommentCreateListAPIView,
    CommentRetrieveUpdateDeleteAPIView,
    ReplyCreateListAPIView,
    ReplyRetrieveUpdateDeleteAPIView,
    comment_downvote,
    comment_upvote,
    post_downvote,
    post_upvote,
    reply_downvote,
    reply_upvote,
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
    # Vote
    path("<int:pk>/upvote/", post_upvote),
    path("<int:pk>/downvote/", post_downvote),
    path("<int:post_pk>/comments/<int:pk>/upvote/", comment_upvote),
    path("<int:post_pk>/comments/<int:pk>/downvote/", comment_downvote),
    path(
        "<int:post_pk>/comments/<int:comment_pk>/replies/<int:pk>/upvote/", reply_upvote
    ),
    path(
        "<int:post_pk>/comments/<int:comment_pk>/replies/<int:pk>/downvote/",
        reply_downvote,
    ),
]
