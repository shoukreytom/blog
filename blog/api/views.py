from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blog.api.serializers import PostSerializer
from blog.models import Post


@api_view(['GET',])
def post_detail_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
