from django.contrib import admin

from .models import VideoChat, VideoChatMedia


@admin.register(VideoChat)
class VideoChatAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' , 'is_deleted' , 'is_active' , 'created_at']


@admin.register(VideoChatMedia)
class VideoChatMediaAdmin(admin.ModelAdmin):
    list_display = ['id' , 'get_video_chat_name' , 'is_deleted' , 'is_active' , 'created_at']
