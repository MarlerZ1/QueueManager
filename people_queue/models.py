from django.db import models


# Create your models here.
class SpecificQueue(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(null=True, blank=True)


class QueueMember(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    specific_queue = models.ForeignKey(to=SpecificQueue, on_delete=models.CASCADE)
