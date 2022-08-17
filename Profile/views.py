import json
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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
        return TeacherProfileSerializer(TeacherProfile.objects.get(user=request.user))

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
                    'message': serialized_obj.message,
                    'error_messages': serialized_obj.errors,
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

        get_user = False
        try:
            get_user = request.data['user']
            
        except:
            pass

        if serialized_obj.is_valid() :
            serialized_obj.save()

            if get_user :
                user_serialized = UserSerializer(
                request.user, data=json.loads( request.data['user']), partial=True)
                if user_serialized.is_valid():
                    user_serialized.save()
                
            user_type_profile = {
                'Student': StudentProfile,
                'Tutor': TeacherProfile
            }

            try:
                user_p = user_type_profile[request.user.user_profile.user_type].objects.get(
                    user=request.user)
                user_p.Country = Country.objects.get(id=request.data['Country'])
                user_p.city = City.objects.get(id=request.data['city'])
                user_p.save()
            except:
                pass

            return Response(
                {
                    'message': 'Profile Successfuly Updated',
                    'data':  serialized_obj.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': serialized_obj.error_messages,
                    'error_messages': serialized_obj.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tutors(request):
    all_tutors = TeacherProfile.objects.filter(
        is_approved=True, is_active=True, is_deleted=False)
    serialized = TeacherProfileSerializer(all_tutors, many=True)

    return Response(
        {
            'status': 'OK',
            'message': 'Request Successful',
            'data': serialized.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tutor(request):
    tutor_slug = request.GET.get('slug', None)
    if tutor_slug is None:
        return Response(
            {
                'status': False,
                'message': 'Invalid Data',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        tutor = TeacherProfile.objects.get(
            slug=tutor_slug, is_approved=True, is_active=True, is_deleted=False
            )
    except:
        return Response(
            {
                'status': False,
                'message': 'Tutor Profile not found',
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serialized = TeacherProfileSerializer(tutor)
    data = dict(serialized.data)
    del data['cnic_image']
    del data['cnic_back']
    del data['cnic_number']

    return Response(
        {
            'status': 'OK',
            'message': 'Request Successful',
            'data': data
        },
        status=status.HTTP_200_OK
    )
