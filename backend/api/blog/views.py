from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    GET ---> api/v1/posts/, with 3 optional parms (status, search, count)
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
    queryset = Post.objects.all()

    def get_queryset(self, *args, **kwargs):
        status = self.request.GET.get("status", None)
        search_txt = self.request.GET.get("search", "")
        count = self.request.GET.get("count", None)
        qs = super().get_queryset()
        if status:
            qs = qs.filter(status=status)
        if search_txt:
            query = Q(title__icontains=search_txt) | Q(content__icontains=search_txt)
            qs = qs.filter(query)
        try:
            count = int(count)
            qs = qs[:count]
        except (ValueError, TypeError):
            pass
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


@api_view(['POST', ])
def post_upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes += 1
    post.save()
    data = {
        'success': True
    }
    return Response(data)

@api_view(['POST', ])
def post_downvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.downvotes += 1
    post.save()
    data = {
        'success': True
    }
    return Response(data)

@api_view(['POST', ])
def comment_upvote(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(post.comments, pk=pk)
    comment.upvotes += 1
    comment.save()
    data = {
        'success': True
    }
    return Response(data)

@api_view(['POST', ])
def comment_downvote(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(post.comments, pk=pk)
    comment.downvotes += 1
    comment.save()
    data = {
        'success': True
    }
    return Response(data)

@api_view(['POST', ])
def reply_upvote(request, post_pk, comment_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(post.comments, pk=comment_pk)
    reply = get_object_or_404(comment.replies, pk=pk)
    reply.upvotes += 1
    reply.save()
    data = {
        'success': True
    }
    return Response(data)

@api_view(['POST', ])
def reply_downvote(request, post_pk, comment_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(post.comments, pk=comment_pk)
    reply = get_object_or_404(comment.replies, pk=pk)
    reply.downvotes += 1
    reply.save()
    data = {
        'success': True
    }
    return Response(data)
