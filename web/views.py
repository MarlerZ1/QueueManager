from django.shortcuts import render
from django.views.generic import ListView

from common.view import TitleMixin
from people_queue.models import QueueMember, SpecificQueue
from web.forms import MembersCreationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specific_queue'] = self.kwargs.get('queue_id')
        context['form'] = MembersCreationForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(specific_queue_id=self.kwargs.get('queue_id'))

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = MembersCreationForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.specific_queue = SpecificQueue.objects.get(id=self.kwargs.get("queue_id"))
            member.save()
        return render(request, "web/member_add.html", self.get_context_data())

# def add_new_member(request, queue_id):
#     form = MembersCreationForm(request.POST)
#     if form.is_valid():
#         member = form.save(commit=False)
#         member.specific_queue = SpecificQueue.objects.get(id=queue_id)
#         member.save()
#         context = dict()
#         context['specific_queue'] = queue_id
#         context['form'] = MembersCreationForm
#     return render(request, "web/member_add.html", context)
