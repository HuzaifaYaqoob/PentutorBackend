from django.shortcuts import render
from django.http import JsonResponse, response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def LoginAPI(request):
    data = request.data
    user = authenticate(
        username=data['username'],
        password=data['password']
    )
    if user is not None:
        user_data = UserSerializer(user)
        return Response(
            {
                'status': 'Succes',
                'user': user_data.data,
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            'status': False,
            'message': 'User Not Found'
        },
        status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterAPI(request):

    data = request.data
    print(data)
    try:
        user = User.objects.get(username=data['email'].split('@')[0])
        return Response(
            {
                'status': 'fail',
                'message':  'E-Mail already in-use.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except User.DoesNotExist:
        try:
            create_user = User.objects.create_user(
                username=data['email'].split('@')[0],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
            )
        except:
            return JsonResponse(
                {
                    'status': 'fail',
                    'message': 'Something went wrong'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse(
            {
                'status': 'success',
                'message': 'User Created Successfully'
            },
            status=status.HTTP_201_CREATED
        )


class UserAPI(APIView):

    def get(self, request):
        print(request.user)
        user = UserSerializer(request.user)
        return JsonResponse(
            {
                'success': 'True',
                'response': {
                    'user': user.data,
                }
            },
            status=status.HTTP_200_OK
        )
