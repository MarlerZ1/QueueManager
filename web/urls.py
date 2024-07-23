from django.urls import path

from web.views import QueueListView, MembersListView, change_active_state

app_name = 'web'


urlpatterns = [
    path('', QueueListView.as_view(), name="index"),
    path('members/<int:queue_id>', MembersListView.as_view(), name="members"),
    path('members/change_active_state/<int:queue_id>', change_active_state, name="change_active_state"),
]
