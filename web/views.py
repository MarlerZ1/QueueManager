from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# Create your views here.
class QueueListView(TemplateView):
    template_name = "web/index.html"