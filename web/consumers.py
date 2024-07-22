import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from api.serializers import SpecificQueueSerializer


class SpecificQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("queue_list", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("queue_list", self.channel_name)

    @staticmethod
    def redefine_queue(objects):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "queue_list",
            {
                "type": "queue_message",
                "text": SpecificQueueSerializer(objects, many=True).data
            },
        )

    async def queue_message(self, event):
        await self.send(text_data=json.dumps({"new_objects_list": event["text"]}))
