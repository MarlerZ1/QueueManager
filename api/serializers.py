from rest_framework import serializers

from people_queue.models import SpecificQueue


class SpecificQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificQueue
        fields = ('id', 'name', 'description',)