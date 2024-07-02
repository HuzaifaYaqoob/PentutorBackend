

from rest_framework import serializers

from Authentication.serializers import UserSerializer

from .models import VideoChat, VideoChatMedia, VideoChatSetting
from datetime import datetime


class SettingSerializer(serializers.ModelSerializer):
    muted_participant = UserSerializer(many=True, read_only=True)

    class Meta:
        model = VideoChatSetting
        exclude = ['user', 'video_chat']

class VideoChat_GetSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    allowed_users = UserSerializer(many=True, read_only=True)
    paticipants = UserSerializer(many=True, read_only=True)
    settings = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoChat
        fields = '__all__'

    
    def get_settings(self, obj):
        try:
            all_settings = VideoChatSetting.objects.get(video_chat=obj)
            serialized_obj = SettingSerializer(all_settings)
            return serialized_obj.data
        except Exception as error:
            print(error)
            return {}


class VideoChatClasses(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    allowed_users = UserSerializer(many=True, read_only=True)

    day_name  = serializers.SerializerMethodField()
    start_meeting  = serializers.SerializerMethodField()

    def get_day_name(self, obj):
        return obj.date.strftime("%A")


    def get_start_meeting(self, obj):
        time_now = datetime.now()
        if obj.date == time_now.date():
            if time_now.time() >= obj.start_time and time_now.time() <= obj.end_time:
                return True
        else:
            return False
    
    class Meta:
        model = VideoChat
        fields = ['id', 'host', 'allowed_users', 'day_name', 'start_time', 'end_time', 'start_meeting']
