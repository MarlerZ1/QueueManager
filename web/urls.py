from django.urls import path

from web.views import QueueTemplateView, MembersTemplateView, change_active_state, remove_first_member, StatisticTemplateView

app_name = 'web'

urlpatterns = [
    path('', QueueTemplateView.as_view(), name="index"),
    path('members/<int:queue_id>', MembersTemplateView.as_view(), name="members"),
    path('members/change_active_state/<int:queue_id>', change_active_state, name="change_active_state"),
    path('members/remove_first_member/<int:queue_id>', remove_first_member, name="remove_first_member"),
    path('members/statistics_graph/<int:queue_id>', StatisticTemplateView.as_view(), name="statistics_graph"),
]
