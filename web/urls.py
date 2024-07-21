from django.urls import path

from web.views import QueueListView, MembersListView

app_name = 'web'


urlpatterns = [
    path('', QueueListView.as_view(), name="index"),
    path('members/<int:queue_id>', MembersListView.as_view(), name="members"),
]
