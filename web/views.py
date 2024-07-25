from datetime import timedelta, datetime

from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import ListView, TemplateView

from common.view import TitleMixin
from people_queue.models import QueueMember, SpecificQueue, AnswerTime
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
        context['specific_queue'] = SpecificQueue.objects.get(id=self.kwargs.get('queue_id'))
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
            if member.specific_queue.active:
                member.save()
        return render(request, "web/member_add.html", self.get_context_data())


def change_active_state(request, queue_id):
    queue = SpecificQueue.objects.get(id=queue_id)
    if request.user.is_superuser:
        members = QueueMember.objects.filter(specific_queue_id=queue_id)
        queue.active = not queue.active

        if queue.active and members.exists():
            first = members[0]
            first.start_time = now()
            first.save()
        queue.save()

    return render(request, "web/plug.html")


def remove_first_member(request, queue_id):
    if request.user.is_superuser:
        members = QueueMember.objects.filter(specific_queue_id=queue_id)

        if members.exists():
            now_t = now().time()

            now_delta = timedelta(hours=now_t.hour, minutes=now_t.minute, seconds=now_t.second)
            past_delta = timedelta(hours=members[0].start_time.hour, minutes=members[0].start_time.minute,
                                   seconds=members[0].start_time.second)
            delta = now_delta - past_delta

            AnswerTime.objects.create(specific_queue_id=queue_id, name=members[0].name,
                                      time=(delta + datetime.min).time())
            members[0].delete()

            if members.exists():
                fist = members[0]
                fist.start_time = now()
                fist.save()

    return render(request, 'web/plug.html')


class StatisticTemplateView(TitleMixin, TemplateView):
    template_name = 'web/statistics_graph.html'
    title = 'Queue - Statistic'
    model = AnswerTime
    queue = AnswerTime.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queue_id'] = self.kwargs.get("queue_id")
        return context
