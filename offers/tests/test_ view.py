from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_offer(self):
        response = self.client.get(reverse('offer:add_offer'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/add_offer.html')

    def test_display_offer(self):
        response = self.client.get(reverse('offer:see_offer'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_offer_detail(self):
        response = self.client.get(reverse('offer:offer_details'), kwargs={'result_id': 80})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_detail.html')

    def test_basket(self):
        response = self.client.get(reverse('offer:basket_add'), kwargs={'result_id': 80})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')