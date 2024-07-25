from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.timezone import now


# Create your models here.
class SpecificQueue(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(null=False, default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import SpecificQueueConsumer
        from web.consumers import MembersConsumer
        objects = SpecificQueue.objects.all()
        alredy_exist_versions = objects.filter(id=self.id)

        if (alredy_exist_versions.exists()):
            is_active_updated = self.active != alredy_exist_versions.first().active
        else:
            is_active_updated = False

        super().save(force_insert, force_update, using, update_fields)

        SpecificQueueConsumer.redefine_queue(objects)
        if is_active_updated:
            MembersConsumer.redefine_members(self.id, is_active_updated)


@receiver(post_delete, sender=SpecificQueue)
def specific_queue_page_update_invoker(sender, instance, using, **kwargs):
    from web.consumers import SpecificQueueConsumer
    objects = SpecificQueue.objects.all()
    SpecificQueueConsumer.redefine_queue(objects)


class QueueMember(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    specific_queue = models.ForeignKey(to=SpecificQueue, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import MembersConsumer
        self.start_time = now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        MembersConsumer.redefine_members(self.specific_queue.id)


@receiver(post_delete, sender=QueueMember)
def specific_queue_page_update_invoker(sender, instance, using, **kwargs):
    from web.consumers import MembersConsumer
    MembersConsumer.redefine_members(instance.specific_queue.id)


class AnswerTime(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    time = models.TimeField()
    specific_queue = models.ForeignKey(to=SpecificQueue, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import StatisticConsumer
        super().save(force_insert, force_update, using, update_fields)

        StatisticConsumer.redefine_statistic(self)
        objects = AnswerTime.objects.filter(specific_queue=self.specific_queue)
        if objects.count() > 5:
            objects.first().delete()
