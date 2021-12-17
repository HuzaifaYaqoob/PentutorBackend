import json
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Authentication.serializers import UserSerializer
from Utility.models import City, Country

from .models import StudentProfile, TeacherProfile

from .Serializers import StudentProfileSerializers, TeacherProfileSerializer
# Create your views here.


class ProfileView(APIView):

    def get_StudentProfile(self, request):
        return StudentProfileSerializers(StudentProfile.objects.get(user=request.user))

    def get_TeacherProfile(self, request):
        return TeacherProfileSerializer(StudentProfile.objects.get(user=request.user))

    def get(self, request):
        user_type_serializer = {
            'Student': self.get_StudentProfile,
            'Tutor': self.get_TeacherProfile
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](
            request)
        return Response(
            {
                'message': 'Request Successful',
                'data': serialized_obj.data
            },
            status=status.HTTP_200_OK
        )

    def saveStudentProfile(self, request):
        return StudentProfileSerializers(StudentProfile.objects.get(user=request.user), data=request.data, partial=True)

    def saveTutorProfile(self, request):
        return StudentProfileSerializers(TeacherProfile.objects.get(user=request.user), data=request.data, partial=True)

    def post(self, request):
        user_type_serializer = {
            'Student': self.saveStudentProfile,
            'Tutor': self.saveTutorProfile()
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](
            request)

        if(serialized_obj.is_valid()):
            serialized_obj.save()
            return Response(
                {
                    'message': 'Profile Successfuly Created',
                    'data': serialized_obj.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'message': serialized_obj.message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        user_type_serializer = {
            'Student': self.saveStudentProfile,
            'Tutor': self.saveTutorProfile
        }

        serialized_obj = user_type_serializer[request.user.user_profile.user_type](
            request)
        user_serialized = UserSerializer(
            request.user, data=json.loads(request.data['user']), partial=True)

        if serialized_obj.is_valid() & user_serialized.is_valid():
            user_serialized.save()
            serialized_obj.save()

            user_p  = StudentProfile.objects.get(user = request.user)
            user_p.Country = Country.objects.get(id = request.data['Country'])
            user_p.city = City.objects.get(id = request.data['city'])
            user_p.save()

            return Response(
                {
                    'message': 'Profile Successfuly Updated',
                    'data':  serialized_obj.data
                },
                status=status.HTTP_200_OK
            )
        else:
            print(serialized_obj.error_messages)
            return Response(
                {
                    'message': serialized_obj.error_messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )
