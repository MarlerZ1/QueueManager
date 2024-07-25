from rest_framework import serializers

from people_queue.models import SpecificQueue, QueueMember, AnswerTime


class SpecificQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificQueue
        fields = ('id', 'name', 'description', 'active')


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueMember
        fields = ('id', 'name', 'specific_queue')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTime
        fields = ('id', 'name', 'specific_queue', 'time')
