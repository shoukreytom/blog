from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from blog.api.serializers import PostSerializer
from blog.models import Post


class PostsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class PostApiList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('status',)
    search_fields = ('title', 'content', )

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status is None:
            return super().get_queryset()
        else:
            if status.lower() == 'published':
                return Post.published.all()
            elif status.lower() == 'draft':
                return Post.objects.filter(status='draft')
            else:
                return super().get_queryset()


class PostDestroyApi(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['GET', ])
def post_detail_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
