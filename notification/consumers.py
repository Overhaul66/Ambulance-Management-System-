import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        if user.is_authenticated:
            self.group_name = f"user_{user.id}"

            # Join the user's group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()

            print(f"Connected to: {self.group_name}")
        else:
            await self.close()  # Reject connection if not authenticated

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            print(f"Disconnected from: {self.group_name}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            json_msg = json.loads(text_data)
            msg = json_msg.get('message')
            receiver_id = json_msg.get('receiver_id')

            if not msg or not receiver_id:
                await self.send(text_data=json.dumps({"error": "Missing receiver_id or message"}))
                return

            target_group = f"user_{receiver_id}"

            await self.channel_layer.group_send(
                target_group,
                {
                    "type": "notify",
                    "message": msg
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
