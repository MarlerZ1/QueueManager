import json
from asyncio import sleep

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.serializers import SpecificQueueSerializer
from people_queue.models import SpecificQueue


def get_serialized_specific_queue(object):
    return SpecificQueueSerializer(object, many=True).data

class SpecificQueueConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        while True:
            objects = SpecificQueue.objects.all()


            await self.send(json.dumps({"new_objects_list": await sync_to_async(get_serialized_specific_queue)(objects)}))
            await sleep(3)
