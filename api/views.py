from rest_framework.viewsets import ModelViewSet

from api.serializers import SpecificQueueSerializer
from people_queue.models import SpecificQueue


class SpecificQueueModelViewSet(ModelViewSet):
    queryset = SpecificQueue.objects.all()
    serializer_class = SpecificQueueSerializer
