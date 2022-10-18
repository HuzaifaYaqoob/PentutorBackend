import json
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from Authentication.serializers import UserSerializer
from Utility.models import City, Country

from .models import StudentProfile, TeacherProfile, UserExperience, UserQualification

from .Serializers import StudentProfileSerializers, TeacherProfileSerializer, UserExperienceSerializer, UserQualificationSerializer
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
        return TeacherProfileSerializer(TeacherProfile.objects.get(user=request.user), data=request.data, partial=True)

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
                user_p.profile_image = request.data['profile_image']
                user_p.Country = Country.objects.get(id=request.data['Country'])
                user_p.city = City.objects.get(id=request.data['city'])
                user_p.save()
            except Exception as err:
                print(err)
                pass


            user_type_serializer_output = {
                'Student': lambda: StudentProfileSerializers(StudentProfile.objects.get(user=request.user)),
                'Tutor':  lambda : TeacherProfileSerializer(TeacherProfile.objects.get(user=request.user))
            }
            output_serialized = user_type_serializer_output[request.user.user_profile.user_type]()

            return Response(
                {
                    'message': 'Profile Successfuly Updated',
                    'data':  output_serialized.data
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
def get_featured_tutors(request):
    tutors = TeacherProfile.objects.filter(
           is_approved=True,
           is_active=True, 
           is_deleted=False,
           is_featured=True
        )
    serialized = TeacherProfileSerializer(tutors, many=True)
    return Response(
        {
            'status': 'OK',
            'message': 'Request Successful',
            'tutors': serialized.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_qualification(request):
    degree = request.data.get('degree', None)
    subject = request.data.get('subject', None)
    year = request.data.get('year', None)
    institute = request.data.get('institute', None)

    if not all([degree, subject, year, institute]):
        return Response(
            {
                'status': 'False',
                'message': 'Invalid data',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    obj = UserQualification.objects.create(
        user = request.user,
        degree = degree,
        subject = subject,
        passing_year = year,
        institute = institute
    )

    data = UserQualificationSerializer(obj)

     
    return Response(
        {
            'status': 'OK',
            'message': 'Request Successful',
            'data': data.data
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_experience(request):

    position = request.data.get('position', None)
    from_date = request.data.get('from_date', None)
    to_date = request.data.get('to_date', None)
    institute = request.data.get('institute', None)
    exprience_years = request.data.get('exprience_years', None)

    if not all([position, from_date, to_date, institute, exprience_years]):
        return Response(
            {
                'status': 'False',
                'message': 'Invalid data',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    obj = UserExperience.objects.create(
        user = request.user,
        position = position,
        from_date = from_date,
        to_date = to_date,
        institute = institute,
        exprience_years = exprience_years
    )

    data = UserExperienceSerializer(obj)

     
    return Response(
        {
            'status': 'OK',
            'message': 'Request Successful',
            'data': data.data
        },
        status=status.HTTP_201_CREATED
    )

