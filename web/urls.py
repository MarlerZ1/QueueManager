from django.urls import path

from web.views import QueueListView

app_name = 'web'


urlpatterns = [
    path('', QueueListView.as_view(), name="index"),
]
