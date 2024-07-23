from rest_framework import serializers

from people_queue.models import SpecificQueue, QueueMember


class SpecificQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificQueue
        fields = ('id', 'name', 'description',)


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueMember
        fields = ('id', 'name', 'specific_queue')
