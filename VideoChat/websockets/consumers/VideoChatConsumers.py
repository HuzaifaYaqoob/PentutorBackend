

from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class VideoChatConsumers(WebsocketConsumer):

    def __init__(self):
        self.channel_base = 'video_chat_user_socket_' ## adding chat ID and userID
        # self.channel_base = 'video_chat_user_socket_<videochat_id>_<user_id>' 

        
    
    def connect(self):
        # self.channel_base += 'chatid'
        # self.channel_base += 'userid'
        self.accept()
        # async_to_sync(self.channel_layer.group_add)(
        #     self.channel_base,
        #     self.channel_name
        # )

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        r_type = text_data['type']

        types_ = {
            'NEW_CONNECTION_REQUEST' : self.new_connection_request,
            'NEW_CONNECTION_ACCEPTED' : self.new_connection_accepted
        }

        if r_type in types_:
            types_[r_type]()
        print('gonna receive')

    def disconnect(self, code):
        print('disconnected')




    
    def new_connection_request(self):
        print('NEW CONNECTION REQUEST RECEIEVE')
    
    def new_connection_accepted(self):
        print('NEW CONNECTION ACCEPTED')


class ActivatedVideoChat(WebsocketConsumer):

    # def __init__(self):
    #     self._types = {
    #         'NEW_CONNECTED_ADDED' : self.new_connection_added
    #     }

    def connect(self):
        print('gonna accept')
        self.accept()
        self.send('hellow')

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        print('gonna receive')

    def disconnect(self, code):
        print('disconnected')




    def new_connection_added(self):
        print('ADDED NEW CONNECTIOn')