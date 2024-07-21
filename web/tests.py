from http import HTTPStatus

from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from people_queue.models import SpecificQueue, QueueMember


# Create your tests here.
class QueueListTestCase(TestCase):
    def test_success_empty(self):
        path = reverse('web:index')
        response = self.client.get(path)

        self.assertTemplateUsed(response, 'web/index.html')
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data["title"], "Queue List")
        self.assertEquals(list(response.context_data["object_list"]), [])

    def test_success(self):
        SpecificQueue.objects.create(name="Test Queue")
        SpecificQueue.objects.create(name="Test2", description="Test desc")

        path = reverse('web:index')
        response = self.client.get(path)


        self.assertTemplateUsed(response, 'web/index.html')
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data["title"], "Queue List")
        self.assertEquals(list(response.context_data["object_list"]), list(SpecificQueue.objects.all()))


class MemberListTestCase(TestCase):
    def setUp(self):
        SpecificQueue.objects.create(name="Test Queue")

    def test_success(self):
        path = reverse('web:members', args=(1, ))
        response = self.client.get(path)

        self.assertTemplateUsed(response, 'web/members.html')
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data["title"], "Members List")
        self.assertEquals(list(response.context_data["object_list"]), list(QueueMember.objects.all()))
