

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
            self.accept()
            async_to_sync(self.channel_layer.group_add)(
                self.channel_base,
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
            # 'CONNECTION_ACCEPTED' : self.connection_accepted
        }

        if r_type in types_:
            types_[r_type]()
        print('gonna receive')

    def disconnect(self, code):
        print('disconnected')

    def chat_message(self, event):
        self.send(json.dumps(event['message']))

    
    def new_connection_request(self):
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
                    'message' : f'{self.user.username} want to join this meeting.'
                }
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
        if self.user.is_authenticated and get_chat is not None and self.user in get_chat.allowed_users.all():
            self.vidChat = get_chat
            self.accept()
            self.activated_vc_channel_base = f'active-video-chat-{self.video_chat_id}'

            async_to_sync(self.channel_layer.group_add)(
                self.activated_vc_channel_base,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        r_type = data['type']

        if r_type == 'NEW_CONNECTION_ACCEPTED':
            self.new_connection_accepted(data['message'])
        elif r_type == 'CONNECTION_REJECTED':
            self.connection_rejected(data['message'])

    def disconnect(self, code):
        print('disconnected')


    def chat_message(self, event):
        message = event['message']

        self.send(json.dumps(message))

    def new_connection_accepted(self, message):
        username = message['user']['username']
        email = message['user']['username']
        print(message)
        try:
            get_user = User.objects.get(username=username)
            self.vidChat.paticipants.add(get_user)
            self.vidChat.save()
        except Exception as err:
            print(err)
            # pass

        async_to_sync(self.channel_layer.group_send)(
            f'video-chat-user-socket-{self.video_chat_id}-{username}',
            {
                'type' : 'chat.message',
                'message' : {
                    'type' : 'CONNECTION_ACCEPTED',
                    'message' : f'{self.user.username} has accepted to join you this meeting.'
                }
            }
        )


    def connection_rejected(self, message):
        pass


    def new_connection_added(self):
        print('ADDED NEW CONNECTIOn')