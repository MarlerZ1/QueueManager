from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class SpecificQueue(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from web.consumers import SpecificQueueConsumer
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        objects = SpecificQueue.objects.all()
        SpecificQueueConsumer.redefine_queue(objects)


@receiver(post_delete, sender=SpecificQueue)
def specific_queue_page_update_invoker(sender, instance, using, **kwargs):
    from web.consumers import SpecificQueueConsumer
    objects = SpecificQueue.objects.all()
    SpecificQueueConsumer.redefine_queue(objects)


class QueueMember(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    specific_queue = models.ForeignKey(to=SpecificQueue, on_delete=models.CASCADE)
