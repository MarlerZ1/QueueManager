import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from api.serializers import SpecificQueueSerializer, MembersSerializer, StatisticSerializer
from people_queue.models import QueueMember, SpecificQueue, AnswerTime


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

    async def receive(self, text_data=None, bytes_data=None):
        await sync_to_async(SpecificQueueConsumer.redefine_queue)(SpecificQueue.objects.all())


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

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        await sync_to_async(MembersConsumer.redefine_members)(text_data_json["specific_queue"], True)


class StatisticConsumer(AsyncWebsocketConsumer):

    @staticmethod
    def initial_objects_sender(queue_id):
        all_objects = AnswerTime.objects.filter(specific_queue_id=queue_id).order_by('-id')

        if len(all_objects) >= 5:
            requider_objects = all_objects[:5]
        else:
            requider_objects = all_objects

        requider_objects = list(requider_objects)[::-1]

        for object in requider_objects:
            StatisticConsumer.redefine_statistic(object)

    async def connect(self):
        self.queue_id = self.scope['url_route']['kwargs']['queue_id']

        await self.channel_layer.group_add("statistic_" + str(self.queue_id), self.channel_name)
        await self.accept()
        await sync_to_async(StatisticConsumer.initial_objects_sender)(self.queue_id)

    async def disconnect(self, code):
        await self.channel_layer.group_discard("statistic_" + str(self.queue_id), self.channel_name)

    @staticmethod
    def redefine_statistic(answer_object):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "statistic_" + str(answer_object.specific_queue.id),
            {
                "type": "statistic_message",
                "object": StatisticSerializer(answer_object).data,
            },
        )

    async def statistic_message(self, event):
        object = event["object"]

        hourst, minuts, seconds = map(int, object['time'].split(':'))

        minuts += seconds / 60 + hourst * 60
        object['time'] = minuts

        await self.send(text_data=json.dumps({"object": object}))
