

from rest_framework import serializers

from .models import VideoChat, VideoChatMedia

class VideoChat_GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChat
        fields = '__all__'