from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
from .models import Job, ApplyJob
from Profile.models import TeacherProfile
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_jobs(request):
    jobs = Job.objects.filter(user=request.user)
    serializer = serializers.JobGetMySerializer(jobs, many=True)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jobs(request):
    jobs = Job.objects.filter(is_deleted=False)
    serializer = serializers.JobGetAllSerializer(jobs, many=True)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_single_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, is_deleted=False)
    except:
        pass
    data = serializers.JobGetAllSerializer(job).data
    
    if request.user.is_authenticated:
        if request.user == job.user:
            applied_jobs = []
            for apl_job in ApplyJob.objects.filter(job = job):
                try:
                    tutor_profile = TeacherProfile.objects.get(user=apl_job.user)
                except Exception as err:
                    tutor_id = None
                else:
                    tutor_id = f'ID-PT{tutor_profile.teacher_id}'
                applied_jobs.append({
                    'message' : apl_job.message,
                    'created_at' : str(apl_job.created_at),
                    'tutor_id' : tutor_id,
                })
            data['applied_jobs'] = applied_jobs
    return Response({**data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, is_deleted=False)
    except:
        pass

    job_apply = ApplyJob.objects.create(
        user=request.user, 
        job=job,
        message = request.data.get('message'),
    )
    if request.FILES.get('resume', None):
        job_apply.resume = request.FILES.get('resume')
        job_apply.save()
    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    try:
        request.data._mutable = True
    except:
        pass
    request.data['user'] = str(request.user.id)
    serializer = serializers.JobCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)
    return Response({'status' : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)