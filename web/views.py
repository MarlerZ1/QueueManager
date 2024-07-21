from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from people_queue.models import QueueMember, SpecificQueue


# Create your views here.
class QueueListView(ListView):
    template_name = "web/index.html"
    model = SpecificQueue
    queryset = SpecificQueue.objects.all()

class MembersListView(ListView):
    template_name = "web/index.html"
    model = QueueMember
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(specific_queue_id=self.kwargs.get('queue_id'))