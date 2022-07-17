

from email import message
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

from VideoChat.models import VideoChat
from django.contrib.auth.models import User
class VideoChatConsumers(WebsocketConsumer):

    # all types 
    # CONNECTED
    # NEW_CONNECTION_REQUEST
    # NEW_CONNECTION_REQUEST
    # CONNECTION_ACCEPTED

    activated_vc_channel_base = 'active-video-chat-<videochat_id_here>'
    
    def connect(self):
        self.user = self.scope['user']
        self.video_chat_id = self.scope['url_route']['kwargs']['videochat_id']

        try:
            get_chat = VideoChat.objects.get(id=self.video_chat_id)
        except:
            get_chat = None
        if self.user.is_authenticated and get_chat is not None:
            self.vidChat = get_chat
            self.channel_base = f'video-chat-user-socket-{self.video_chat_id}-{self.user.username}'
            self.channel_base2 = f'video-chat-user-socket-{self.video_chat_id}'
            self.accept()
            async_to_sync(self.channel_layer.group_add)(
                self.channel_base,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_add)(
                self.channel_base2,
                self.channel_name
            )

            async_to_sync(self.channel_layer.group_send)(
                self.channel_base,
                {
                    'type' : 'chat.message',
                    'message' : {
                        'type' : 'CONNECTED',
                        'message' : 'Connected to Video chat'
                    }
                }
            )


    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        r_type = text_data['type']

        types_ = {
            'NEW_CONNECTION_REQUEST' : self.new_connection_request,
            'ICE_CANDIDATE' : self.onIceCandidate,
            'CONNECTION_ACCEPTED' : self.request_approved,
            'CONNECTION_REJECTED' : self.request_declined,
        }

        if r_type in types_:
            types_[r_type](text_data)

    def disconnect(self, code):
        print('vid chat not active disconnected', code)

    def chat_message(self, event):
        self.send(json.dumps(event['message']))

    def send_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.channel_base,
            {
                'type' : 'chat_message',
                'message' : message
            }
        )

    def new_connection_request(self, message):
        async_to_sync(self.channel_layer.group_send)(
            f'active-video-chat-{self.video_chat_id}',
            {
                'type' : 'chat.message',
                'message' : {
                    'type' : 'NEW_CONNECTION_REQUEST',
                    'user' : {
                        'username' : self.user.username,
                        'email' : self.user.email
                    },
                    'chat' : {
                        'name' : self.vidChat.name,
                        'host' : {
                            'username' : self.vidChat.host.username,
                            'email' : self.vidChat.host.email,
                            'id' : self.vidChat.host.id,
                        }
                    },
                    'message' : f'{self.user.username} want to join this meeting.',
                    'offer' : message['offer']
                }
            }
        )

    def onIceCandidate(self, message):
        async_to_sync(self.channel_layer.group_send)(
            f'active-video-chat-{self.video_chat_id}',
            {
                'type' : 'chat_message',
                'message' : message
            }
        )
        async_to_sync(self.channel_layer.group_send)(
            self.channel_base2,
            {
                'type' : 'chat_message',
                'message' : message
            }
        )

    def request_approved(self, message):
        username = message['requested']['username']
        # email = message['user']['username']
        try:
            get_user = User.objects.get(username=username)
            self.vidChat.allowed_users.add(get_user)
            self.vidChat.save()
        except Exception as err:
            print(err)
            # pass

        message['active_users'] = self.vidChat.participants.all()
        async_to_sync(self.channel_layer.group_send)(
            f'video-chat-user-socket-{self.video_chat_id}-{username}',
            {
                'type' : 'chat.message',
                'message' : message,
            }
        )
    
    def request_declined(self, message):
        username = message['user']['username']

        async_to_sync(self.channel_layer.group_send)(
            f'video-chat-user-socket-{self.video_chat_id}-{username}',
            {
                'type' : 'chat.message',
                'message' : message
            }
        )
    











class ActivatedVideoChat(WebsocketConsumer):

    # NEW_CONNECTION_ACCEPTED
    

    def connect(self):
        self.user = self.scope['user']
        self.video_chat_id = self.scope['url_route']['kwargs']['videochat_id']

        try:
            get_chat = VideoChat.objects.get(id=self.video_chat_id)
        except:
            get_chat = None
        # if self.user.is_authenticated and get_chat is not None and self.user in get_chat.allowed_users.all():
        if self.user.is_authenticated and get_chat is not None:
            self.vidChat = get_chat
            self.accept()
            if self.user.username == get_chat.host.username:
                try:
                    self.vidChat.paticipants.add(self.user)
                    self.vidChat.save()
                except:
                    pass
            self.activated_vc_channel_base = f'active-video-chat-{self.video_chat_id}'

            async_to_sync(self.channel_layer.group_add)(
                self.activated_vc_channel_base,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        r_type = data['type']

        if r_type == 'NEW_CONNECTION_REQUEST':
            async_to_sync(self.channel_layer.group_send)(
                f'video-chat-user-socket-{self.video_chat_id}-{self.vidChat.host.username}',
                {
                    'type' : 'chat.message',
                    'message' : data
                }
            )
        elif r_type == 'CONNECTION_ACCEPTED':
            self.new_connection_accepted(data)
        elif r_type == 'CONNECTION_REJECTED':
            self.connection_rejected(data)
        elif r_type == 'ICE_CANDIDATE':
            self.IceCandidate(data)
        elif r_type == 'NEW_USER_JOINED_VIDEO_CHAT':
            self.NewUserJoinedVideoChat(data)
        elif r_type == 'NEW_USER_JOINED_VIDEO_CHAT_APPROVED':
            self.NewUserJoinedVideoChatApproved(data)
        elif r_type == 'CUSTOM_OFFER':
            async_to_sync(self.channel_layer.group_send)(
                self.activated_vc_channel_base,
                {
                    'type' : 'chat.message',
                    'message' : data
                }
            )
        elif r_type == 'CUSTOM_ANSWER':
            async_to_sync(self.channel_layer.group_send)(
                self.activated_vc_channel_base,
                {
                    'type' : 'chat.message',
                    'message' : data
                }
            )
        elif r_type == 'USER_LEFT_MEETING':
            try:
                get_user = User.objects.get(username=self.user.username)
                self.vidChat.paticipants.remove(get_user)
                self.vidChat.save()
            except Exception as err:
                print('EERRR :: ', err)
                pass
            async_to_sync(self.channel_layer.group_send)(
                self.activated_vc_channel_base,
                {
                    'type' : 'chat.message',
                    'message' : data
                }
            )
        elif r_type == 'CHAT_NEW_MESSAGE':
            async_to_sync(self.channel_layer.group_send)(
                self.activated_vc_channel_base,
                {
                    'type' : 'chat.message',
                    'message' : data
                }
            )

    def disconnect(self, code):
        try:
            get_user = User.objects.get(username=self.user.username)

            self.vidChat.paticipants.remove(get_user)
            print('//////////////////// user removed', get_user)
            self.vidChat.save()
        except Exception as err:
            print('EERRR :: ', err)
            pass
        async_to_sync(self.channel_layer.group_send)(
            self.activated_vc_channel_base,
            {
                'type' : 'chat.message',
                'message' : {
                    'user' : str(self.user)
                }
            }
        )
        print('disconnected', code)


    def chat_message(self, event):
        message = event['message']

        self.send(json.dumps(message))

    def new_connection_accepted(self, message):
        username = message['requested']['username']
        # try:
            # get_user = User.objects.get(username=username)
            # self.vidChat.allowed_users.add(get_user)
            # self.vidChat.save()
        # except Exception as err:
        #     print(err)

        async_to_sync(self.channel_layer.group_send)(
            f'video-chat-user-socket-{self.video_chat_id}-{username}',
            {
                'type' : 'chat.message',
                'message' : message
            }
        )


    def connection_rejected(self, message):
        username = message['user']['username']

        async_to_sync(self.channel_layer.group_send)(
            f'video-chat-user-socket-{self.video_chat_id}-{username}',
            {
                'type' : 'chat.message',
                'message' : message
            }
        )


    def IceCandidate(self, message):
        # username = message['send_to']['username']
        async_to_sync(self.channel_layer.group_send)(
            self.activated_vc_channel_base,
            {
                'type' : 'chat.message',
                'message' : message
            }
        )

    def NewUserJoinedVideoChat(self, message):
        try:
            get_user = User.objects.get(username=self.user.username)
            self.vidChat.paticipants.add(get_user)
            self.vidChat.save()
        except Exception as err:
            print('ERROR ::::: ' , err)
        async_to_sync(self.channel_layer.group_send)(
            self.activated_vc_channel_base,
            {
                'type' : 'chat.message',
                'message' : message
            }   
        )

    def NewUserJoinedVideoChatApproved(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.activated_vc_channel_base,
            {
                'type' : 'chat.message',
                'message' : message
            }   
        )