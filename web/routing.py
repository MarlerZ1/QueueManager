from django.urls import path

from web.consumers import SpecificQueueConsumer, MembersConsumer

ws_urlpatterns = [
    path('ws/queue/', SpecificQueueConsumer.as_asgi()),
    path('ws/members/<int:queue_id>', MembersConsumer.as_asgi()),
]