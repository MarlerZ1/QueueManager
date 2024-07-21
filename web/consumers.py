import json
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

from people_queue.models import SpecificQueue


class SpecificQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            # await self.send(json.dumps({"new_objects_list": SpecificQueue.objects.all()}))
            await sleep(1)
