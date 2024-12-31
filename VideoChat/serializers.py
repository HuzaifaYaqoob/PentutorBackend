

from rest_framework import serializers

from Authentication.serializers import UserSerializer
from Profile.models import Profile
from django.contrib.auth.models import User
from .models import VideoChat, VideoChatMedia, VideoChatSetting, DemoCallRequest, DemoClassTimeSlot
from Profile.models import TeacherProfile
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

    day_name  = serializers.SerializerMethodField()
    start_meeting  = serializers.SerializerMethodField()
    partner  = serializers.SerializerMethodField()

    def get_day_name(self, obj):
        return obj.date.strftime("%A")

    def get_partner(self, obj):
        request = self.context.get('request', None)
        if request:
            user = None
            for u in obj.allowed_users.all():
                if str(u.id) != str(request.user.id):
                    user = u
                    break
            
            if not user:
                return None
            try:
                profile = Profile.objects.get(user=user)
            except Exception as err:
                return f'{user.first_name} {user.last_name}'
            else:
                if profile.user_type == 'Student':
                    return f'ID-PTS{str(profile.slug).split("-")[0].upper()}'
                else:
                    return f'ID-PT{str(profile.slug).split("-")[0]}'
        return None


    def get_start_meeting(self, obj):
        time_now = datetime.now()
        if obj.date == time_now.date():
            if time_now.time() >= obj.start_time and time_now.time() <= obj.end_time:
                return True
        else:
            return False
    
    class Meta:
        model = VideoChat
        fields = ['id', 'name', 'host', 'date', 'day_name', 'start_time', 'end_time', 'partner', 'start_meeting']

class DemoClassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id']


class DemoCallRequestSerializer(serializers.ModelSerializer):
    user = DemoClassUserSerializer(read_only=True)

    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        call_time = DemoClassTimeSlot.objects.filter(demo_class=obj).order_by('-created_at').first()
        return {
            'date' : call_time.selected_date,
            'time' : call_time.selected_time,
            'id' : call_time.id
        }

    def to_representation(self, instance):
        data = super(DemoCallRequestSerializer, self).to_representation(instance)
        if instance.video_room:
            data['video_room'] = instance.video_room.name
        
        try:
            teacher_profile = TeacherProfile.objects.get(user=instance.tutor)
        except:
            pass
        else:
            data['tutor_id'] = f'ID-PT{teacher_profile.teacher_id}'
        return data
    class Meta:
        model = DemoCallRequest
        fields = '__all__'