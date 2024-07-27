from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import *
from people_queue.models import SpecificQueue


class SpecificQueueModelViewSet(ModelViewSet):
    queryset = SpecificQueue.objects.all()
    serializer_class = SpecificQueueSerializer


class MembersModelViewSet(ModelViewSet):
    queryset = QueueMember.objects.all()
    serializer_class = MembersSerializer

    def get_queryset(self):
        req = self.request
        specific_queue_filter = req.query_params.get('specific_queue')
        if specific_queue_filter:
            self.queryset = self.queryset.filter(specific_queue=specific_queue_filter)
            return self.queryset
        else:
            return self.queryset
