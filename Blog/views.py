from django.shortcuts import render

from Blog.serializers import BlogPostSerializer

from .models import BlogPost

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_posts(request):
    all_posts = BlogPost.objects.all()
    serialized = BlogPostSerializer(all_posts, many=True)
    return Response({'data' : serialized.data},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_single_blog(request):
    slug_id = request.GET.get('slug', None)
    try:
        post = BlogPost.objects.get(slug=slug_id)
    except:
        return Response({'message' : 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serialized = BlogPostSerializer(post)
    return Response({'data' : serialized.data},status=status.HTTP_200_OK)

