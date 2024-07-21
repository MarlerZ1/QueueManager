from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from common.view import TitleMixin
from people_queue.models import QueueMember, SpecificQueue


# Create your views here.
class QueueListView(TitleMixin, ListView):
    template_name = "web/index.html"
    model = SpecificQueue
    queryset = SpecificQueue.objects.all()
    title = "Queue List"
class MembersListView(TitleMixin, ListView):
    template_name = "web/members.html"
    model = QueueMember
    title = "Members List"
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(specific_queue_id=self.kwargs.get('queue_id'))