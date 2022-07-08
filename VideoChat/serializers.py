

from rest_framework import serializers

from Authentication.serializers import UserSerializer

from .models import VideoChat, VideoChatMedia

class VideoChat_GetSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    allowed_users = UserSerializer(many=True, read_only=True)
    paticipants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = VideoChat
        fields = '__all__'