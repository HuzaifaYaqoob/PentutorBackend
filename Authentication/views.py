from django.shortcuts import render
from django.http import JsonResponse, response

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status

from .serializers import UserSerializer

# Create your views here.

@api_view(['POST'])
def LoginAPI(request):
    data = request.data
    user = authenticate(
        username = data['username'],
        password = data['password']
        )
    if user is not None:
        user_data = UserSerializer(user)
        return Response(
            {
                'status' : 'Succes',
                'user' : user_data.data,
            },
            status = status.HTTP_201_CREATED
        )

    return Response(
        {
            'status' : False,
            'message' : 'User Not Found'
        },
        status = status.HTTP_404_NOT_FOUND
    )


def RegisterAPI(request):
    return JsonResponse({
        'Register' :'Register'
    })