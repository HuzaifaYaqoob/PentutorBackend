from django.db import models

from django.contrib.auth.models import User
from uuid import uuid4

from django.utils.timezone import now



class VideoChat(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, unique=True, editable=False, max_length=1000)
    name = models.CharField(max_length=1000, default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True , related_name='video_chats')
    allowed_users = models.ManyToManyField(User, related_name='allowed_video_chats' )
    paticipants = models.ManyToManyField(User, related_name='participated_video_chats')

    created_at = models.DateTimeField(auto_now_add=now)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.id)


class VideoChatMedia(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, unique=True, editable=False, max_length=1000)
    file = models.FileField(upload_to='video_chat_media')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_vchat_medias')
    video_chat = models.ForeignKey(VideoChat, on_delete=models.CASCADE , related_name='video_chat_medias')

    created_at = models.DateTimeField(auto_now_add=now)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.id)


    def get_video_chat_name(self):
        return self.video_chat.name if self.video_chat.name else 'No Name N/A'