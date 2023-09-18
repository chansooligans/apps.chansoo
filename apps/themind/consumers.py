from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        card = text_data_json['card']

        # Send card info to all connected clients
        await self.channel_layer.group_send(
            'cards',  # Group name
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
