

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CourseSerializer

from .models import Course

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_courses(request):
    all_courses = Course.objects.all()
    serialized = CourseSerializer(all_courses, many=True)

    return Response(
        {
            'status' : True,
            'data' : serialized.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    title = request.data['title'] if 'title' in request.data else None
    language = request.data['language'] if 'language' in request.data else None
    category = request.data['category'] if 'category' in request.data else None
    level = request.data['level'] if 'level' in request.data else None
    price = request.data['price'] if 'price' in request.data else None
    description = request.data['description'] if 'description' in request.data else None
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if not title or not language or not category or not level or not price or not description:
        
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.data._mutable = True
    request.data['user'] = user.id
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status' : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_course(request):
    slug = request.data['slug'] if 'slug' in request.data else None
    if not slug:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        course = Course.objects.get(slug=slug)
        if user == course.user:
            course.delete()
            return Response({'status' : True, 'data' : 'Course Deleted Succesfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status' : False, 'data' : 'You have no permission to deleted course!'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_course(request):
    slug = request.data['slug'] if 'slug' in request.data else None
    title = request.data['title'] if 'title' in request.data else None
    language = request.data['language'] if 'language' in request.data else None
    category = request.data['category'] if 'category' in request.data else None
    level = request.data['level'] if 'level' in request.data else None
    price = request.data['price'] if 'price' in request.data else None
    description = request.data['description'] if 'description' in request.data else None
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if not slug:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(slug=slug)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if title:
        course.title = title
    if language:
        course.language = language
    if category:
        course.category = category
    if level:
        course.level = level
    if price:
        course.price = price
        
    if description:
        course.description = description
    course.save()
    serializer = CourseSerializer(course)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)
