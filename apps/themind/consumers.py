from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        card = text_data_json['card']

        # Send card info to all connected clients
        await self.channel_layer.group_send(
            self.room_group_name,  # Group name
            {
                'type': 'send_card',
                'card': card,
            }
        )

    async def send_card(self, event):
        card = event['card']

        # Send card info to WebSocket
        await self.send(text_data=json.dumps({
            'card': card
        }))
