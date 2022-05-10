from django.test import SimpleTestCase
from django.urls import reverse, resolve
from offers.views import (
                    AddOffer, AddPhotos, DisplayOffer,
                    offer_detail, MyOffers, delete_offer,
                    edit_offer, BuyingItem, MyBought,
                    BasketBuyPage,  basket
                        )


class TestUrls(SimpleTestCase):

    def test_add_offer(self):
        url = reverse('offer:add_offer')
        self.assertEqual(resolve(url).func.view_class, AddOffer)

    def test_add_photo(self):
        url = reverse('offer:add_photos')
        self.assertEqual(resolve(url).func.view_class, AddPhotos)

    def test_display_offer(self):
        url = reverse('offer:see_offer')
        self.assertEqual(resolve(url).func.view_class, DisplayOffer)

    def test_offer_detail(self):
        url = reverse('offer:offer_details', kwargs={'result_id': 80})
        self.assertEqual(resolve(url).func, offer_detail)

    def test_my_offer(self):
        url = reverse('offer:my_offer')
        self.assertEqual(resolve(url).func.view_class, MyOffers)

    def test_delete_offer(self):
        url = reverse('offer:delete_offer', kwargs={'result_id': 80})
        self.assertEqual(resolve(url).func, delete_offer)

    def test_edit_offer(self):
        url = reverse('offer:edit_offer', kwargs={'result_id': 80})
        self.assertEqual(resolve(url).func, edit_offer)

    def test_buying_item(self):
        url = reverse('offer:buy_item')
        self.assertEqual(resolve(url).func.view_class, BuyingItem)

    def test_my_bought(self):
        url = reverse('offer:bought')
        self.assertEqual(resolve(url).func.view_class, MyBought)

    def test_basket_buy(self):
        url = reverse('offer:basket')
        self.assertEqual(resolve(url).func.view_class, BasketBuyPage)

    def test_basket_add(self):
        url = reverse('offer:basket_add', kwargs={'offer_id': 80})
        self.assertEqual(resolve(url).func, basket)
