from django.urls import path

from web.consumers import SpecificQueueConsumer

ws_urlpatterns = [
    path('ws/graph/', SpecificQueueConsumer.as_asgi())
]