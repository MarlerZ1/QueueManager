from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class SpecificQueue(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(null=False, default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import SpecificQueueConsumer
        from web.consumers import MembersConsumer

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        objects = SpecificQueue.objects.all()
        SpecificQueueConsumer.redefine_queue(objects)
        MembersConsumer.redefine_members(self.id)


@receiver(post_delete, sender=SpecificQueue)
def specific_queue_page_update_invoker(sender, instance, using, **kwargs):
    from web.consumers import SpecificQueueConsumer
    objects = SpecificQueue.objects.all()
    SpecificQueueConsumer.redefine_queue(objects)


class QueueMember(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    specific_queue = models.ForeignKey(to=SpecificQueue, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import MembersConsumer
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        MembersConsumer.redefine_members(self.specific_queue.id)


@receiver(post_delete, sender=QueueMember)
def specific_queue_page_update_invoker(sender, instance, using, **kwargs):
    from web.consumers import MembersConsumer
    MembersConsumer.redefine_members(instance.specific_queue.id)
