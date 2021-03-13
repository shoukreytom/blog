from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from django.db.models import Q
from blog.models import Comment, Post, Reply
from .serializers import PostSerializer, CommentSerializer, ReplySerializer
from .utils import PostListPaginator


""" METHODS:
    GET ---> api/v1/posts/, with 2 optional parms (status, search)
    POST --> api/v1/posts/

    GET --> api/v1/posts/id/
    PUT --> api/v1/posts/id/
    DELETE --> api/v1/posts/id/
"""


class PostCreateListAPIView(CreateModelMixin, ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = PostSerializer
    pagination_class = PostListPaginator

    def get_queryset(self):
        qs = Post.objects.all()
        status = self.request.GET.get("status", None)
        search_txt = self.request.GET.get("search", "")
        search_query = Q(title__icontains=search_txt) | Q(content__icontains=search_txt)
        if status and status.lower() == "published":
            qs = Post.published.all().filter(search_query)
        if status and status.lower() == "draft":
            qs = Post.drafted.all().filter(search_query)
        return qs

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDeleteAPIView(
    DestroyModelMixin, UpdateModelMixin, RetrieveAPIView
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


""" METHODS:
    GET ---> api/v1/posts/post_id/comments/
    POST --> api/v1/posts/post_id/comments/

    GET --> api/v1/posts/post_id/comments/id/
    PUT --> api/v1/posts/post_id/comments/id/
    DELET --> api/v1/posts/post_id/comments/id/
"""


class CommentCreateListAPIView(CreateModelMixin, ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk", None)
        post = get_object_or_404(Post, pk=post_pk)
        qs = post.comments.all()
        status = self.request.GET.get("status", None)
        if status and status.lower() == "published":
            qs = post.comments.published.all()
        if status and status.lower() == "draft":
            qs = post.comments.drafted.all()
        return qs

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_pk", None)
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(author=self.request.user, post=post)


class CommentRetrieveUpdateDeleteAPIView(
    DestroyModelMixin, UpdateModelMixin, RetrieveAPIView
):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk", None)
        post = get_object_or_404(Post, pk=post_pk)
        qs = post.comments.all()
        return qs


""" METHODS:
    GET --> api/v1/posts/post_id/comments/comment_id/replies/
    POST --> api/v1/posts/post_id/comments/comment_id/replies/

    GET  --> api/v1/posts/post_id/comments/comment_id/replies/id/
    PUT  --> api/v1/posts/post_id/comments/comment_id/replies/id/
    DELETE --> api/v1/posts/post_id/comments/comment_id/replies/id/
"""


class ReplyCreateListAPIView(CreateModelMixin, ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    serializer_class = ReplySerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk", None)
        comment_pk = self.kwargs.get("comment_pk", None)
        post = get_object_or_404(Post, pk=post_pk)
        comments = post.comments.all()
        comment = get_object_or_404(comments, pk=comment_pk)
        return comment.replies.all()

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post_pk", None)
        comment_pk = self.kwargs.get("comment_pk", None)
        post = get_object_or_404(Post, pk=post_pk)
        comments = post.comments.all()
        comment = get_object_or_404(comments, pk=comment_pk)
        serializer.save(author=self.request.user, comment=comment)


class ReplyRetrieveUpdateDeleteAPIView(
    DestroyModelMixin, UpdateModelMixin, RetrieveAPIView
):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
