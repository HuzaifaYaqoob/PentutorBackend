

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
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