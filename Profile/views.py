from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .Serializers import StudentProfileSerializers, TeacherProfileSerializer
# Create your views here.



class ProfileView(APIView):

    def get(self, request):
        user_type_serializer = {
            'Student' : StudentProfileSerializers,
            'Tutor' : TeacherProfileSerializer
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](request.user.user_profile)
        return Response(
            {
                'message' : 'Request Successful',
                'data' : serialized_obj.data
            },
            status = status.HTTP_200_OK
        )

    def post(self, request):
        user_type_serializer = {
            'Student' : StudentProfileSerializers,
            'Tutor' : TeacherProfileSerializer
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](data=request.data)

        if(serialized_obj.is_valid()):
            serialized_obj.save()
            return Response(
                {
                    'message' : 'Profile Successfuly Created',
                    'data' : serialized_obj.data
                },
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'message' : serialized_obj.message
                },
                status = status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        user_type_serializer = {
            'Student' : StudentProfileSerializers,
            'Tutor' : TeacherProfileSerializer
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](request.user.user_profile , data=request.data)

        if(serialized_obj.is_valid()):
            serialized_obj.save()
            return Response(
                {
                    'message' : 'Profile Successfuly Updated',
                    'data' :  serialized_obj.data
                },
                status = status.HTTP_201_CREATED
            )
        else:
            print(serialized_obj.errors)
            return Response(
                {
                    'message' : serialized_obj.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )