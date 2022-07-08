from django.shortcuts import render


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from .models import VideoChat, VideoChatMedia
from .serializers import VideoChat_GetSerializer


@api_view(['POST'])
def create_video_chat(request):
    name = request.GET.get('name' , None)

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
    vid_chat = VideoChat.objects.create(
        name=name,
        host=request.user,
    )
    vid_chat.allowed_users.add(request.user)
    vid_chat.save()

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
        video_chat = VideoChat.objects.get(id=vChat_id, is_deleted=False, is_active=True)
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