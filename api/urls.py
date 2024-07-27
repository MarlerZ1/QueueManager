from django.urls import path, include
from rest_framework import routers

from api.views import *

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'specific_queues_rest', SpecificQueueModelViewSet)
router.register(r'members_rest', MembersModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
