

from channels.generic.websocket import WebsocketConsumer


class VideoChatConsumers(WebsocketConsumer):

    # def __init__(self):
    #     self._types = {
    #         'NEW_CONNECTION_REQUEST' : self.new_connection_request,
    #         'NEW_CONNECTION_ACCEPTED' : self.new_connection_accepted
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