

from rest_framework import serializers

from Authentication.serializers import UserSerializer

from .models import VideoChat, VideoChatMedia, VideoChatSetting


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

    def get_day_name(self, obj):
        return obj.date.strftime("%A")
    
    class Meta:
        model = VideoChat
        fields = ['id', 'host', 'allowed_users', 'day_name']
