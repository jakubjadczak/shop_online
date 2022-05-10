from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_offer(self):
        response = self.client.get(reverse('offer:add_offer'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/add_offer.html')