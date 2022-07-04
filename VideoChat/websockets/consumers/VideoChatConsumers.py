

from channels.generic.websocket import WebsocketConsumer


class VideoChatConsumers(WebsocketConsumer):
    
    def connect(self):
        print('gonna accept')
        self.accept()
        self.send('hellow')

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        print('gonna receive')

    def disconnect(self, code):
        print('disconnected')


class ActivatedVideoChat(WebsocketConsumer):

    def connect(self):
        print('gonna accept')
        self.accept()
        self.send('hellow')

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        print('gonna receive')

    def disconnect(self, code):
        print('disconnected')