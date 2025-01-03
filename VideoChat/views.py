from django.shortcuts import render

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


from .models import VideoChat, VideoChatSetting, DemoCallRequest, DemoClassTimeSlot
from Profile.models import Profile, TeacherProfile
from django.contrib.auth.models import User
from .serializers import VideoChat_GetSerializer, VideoChatClasses, DemoCallRequestSerializer

from datetime import datetime, timedelta


@api_view(['POST'])
def create_video_chat(request):
    name = request.GET.get('name' , None)
    tutor_slug = request.data.get('slug' , None)
    date = request.data.get('date' , None)
    start_time = request.data.get('start_time' , None)
    end_time = request.data.get('end_time' , None)

    if not request.user.is_authenticated:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Authentication Failed',
                    'error_message' : 'Invalid Token or Login Failed'
                }
            }, status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    if not end_time:
        end_time = datetime.now() + timedelta(minutes=30)
        end_time = end_time.strftime("%H:%M")

    vid_chat = VideoChat.objects.create(
        name=name,
        host=request.user,
        date = date,
        start_time = start_time,
        end_time = end_time
    )
    vid_chat.allowed_users.add(request.user)

    try:
        teacher = TeacherProfile.objects.get(slug = tutor_slug)
    except Exception as err:
        vid_chat.delete()
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Tutor ID',
                    'slug' : tutor_slug,
                    'error_message' : str(err)
                }
            }, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        vid_chat.allowed_users.add(teacher.user)
    vid_chat.save()

    video_chat_setting = VideoChatSetting(
        user = request.user,
        video_chat = vid_chat,
    )

    video_chat_setting.save()

    serialized = VideoChat_GetSerializer(vid_chat)

    return Response(
        {
            'status' : True,
            'response' : {
                'message' : 'Video Chat created successfully.',
                'data' : serialized.data,
                'error_message' : None
            }
        }, status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def get_user_video_chats(request):
    video_chats = VideoChat.objects.filter(
        allowed_users = request.user
    )
    serialized = VideoChatClasses(video_chats, many=True, context={'request' : request})

    return Response(
        {
            'status' : True,
            'response' : {
                'data' : serialized.data
            }
        }
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_chat(request):
    vChat_id = request.GET.get('video_chat_id', None)

    if vChat_id is None:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Data'
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        video_chat = VideoChat.objects.get(
            id=vChat_id, 
            is_deleted=False, 
            is_active=True,

        )
    except Exception as err:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : str(err)
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    else:
        video_settings, created = VideoChatSetting.objects.get_or_create(video_chat=video_chat)
        if video_settings.lock_meeting and request.user not in video_chat.allowed_users.all():
            return Response(
                {
                    'status' : False,
                    'response' : {
                        'message' : 'Video Chat is locked'
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serialized_obj = VideoChat_GetSerializer(video_chat)
        return Response(
            {
                'status' : True,
                'response' : {
                    'data' : serialized_obj.data
                }
            },
            status=status.HTTP_200_OK
        )
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def requestTutorDemoClass(request):
    tutor_id = request.POST.get('tutor_id', None)
    selected_date = request.POST.get('selected_date', None)
    selected_time = request.POST.get('selected_time', None)
    if not tutor_id:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Data'
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        tutor = TeacherProfile.objects.get(
            slug = tutor_id
        )
    except Exception as err:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Tutor ID',
                    'error_message' : str(err)
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    demo_class = DemoCallRequest.objects.create(
        user = request.user,
        tutor = tutor.user,
    )

    DemoClassTimeSlot.objects.create(
        user = request.user,
        demo_class = demo_class,
        selected_date = selected_date,
        selected_time = selected_time,
    )

    return Response(
        {
            'status' : True,
            'response' : {
                'message' : 'Demo class requested',
                'error_message' : None
            }
        },
        status=status.HTTP_201_CREATED
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTutorDemoCallRequest(request):
    
    class_requests = DemoCallRequest.objects.filter(
        tutor = request.user,
        # status = 'Requested'
    ).order_by('-created_at')

    serialized = DemoCallRequestSerializer(class_requests, many=True)

    return Response(
        {
            'status' : True,
            'response' : {
                'data' : serialized.data
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStudentDemoCallRequest(request):
    
    class_requests = DemoCallRequest.objects.filter(
        user = request.user,
        # status = 'Requested'
    ).order_by('-created_at')

    serialized = DemoCallRequestSerializer(class_requests, many=True)

    return Response(
        {
            'status' : True,
            'response' : {
                'data' : serialized.data
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AcceptRejectClassRequest(request, class_id):
    slot = request.GET.get('slot', None)

    try:
        class_request = DemoCallRequest.objects.get(
            id = class_id,
            tutor = request.user
        )
        slot = DemoClassTimeSlot.objects.get(
            demo_class = class_request,
            id = slot
        )
    except:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Data'
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    req_status = request.GET.get('status', None)
    
    class_request.status = req_status
    class_request.save()

    if req_status == 'Accepted':
        slot.req_status = 'Approved'
        vid_chat = VideoChat.objects.create(
            name=f'{class_request.user.first_name} requested demo class',
            host=request.user,
            date = slot.selected_date,
            start_time = slot.selected_time,
            # end_time = slot.selected_time + timedelta(minutes=30).time(),
        )
        vid_chat.allowed_users.add(class_request.user)
        vid_chat.allowed_users.add(class_request.tutor)
        vid_chat.save()

        class_request.video_room = vid_chat
        class_request.save()
        video_chat_setting = VideoChatSetting.objects.create(user = request.user,video_chat = vid_chat,)

    elif req_status == 'Rejected':
        slot.req_status = 'Rejected'
    slot.save()
    
    return Response(
        {
            'status' : True,
            'response' : {
                'message' : 'Demo Class Request Updated'
            }
        },
        status=status.HTTP_200_OK
    )

