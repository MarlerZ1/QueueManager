from django.urls import path, include
from rest_framework import routers

from api.views import SpecificQueueModelViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'specific_queues_rest', SpecificQueueModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
