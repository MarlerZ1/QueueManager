import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from api.serializers import SpecificQueueSerializer, MembersSerializer
from people_queue.models import QueueMember, SpecificQueue


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


class MembersConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.queue_id = self.scope['url_route']['kwargs']['queue_id']

        await self.channel_layer.group_add("members_list" + str(self.queue_id), self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("members_list" + str(self.queue_id), self.channel_name)

    @staticmethod
    def redefine_members(specific_queue, is_active_status_changed=False):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "members_list" + str(specific_queue),
            {
                "type": "members_message",
                "text": MembersSerializer(QueueMember.objects.filter(specific_queue_id=specific_queue), many=True).data,
                "new_active": SpecificQueue.objects.get(id=specific_queue).active,
                "is_active_status_changed": is_active_status_changed
            },
        )

    async def members_message(self, event):
        await self.send(text_data=json.dumps({"new_objects_list": event["text"], "new_active": event["new_active"],
                                              "is_active_status_changed": event["is_active_status_changed"]}))
