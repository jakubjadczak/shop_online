from django.urls import path
from .views import (AddOffer, AddPhotos, DisplayOffer,
                    offer_detail, MyOffers, delete_offer,
                    edit_offer, BuyingItem)

app_name = 'offer'

urlpatterns = [
    path('add-offer/', AddOffer.as_view(), name='add_offer'),
    path('add-photos/', AddPhotos.as_view(), name='add_photos'),
    path('see-offer/', DisplayOffer.as_view(), name='see_offer'),
    path('offer-detail-<int:result_id>', offer_detail, name='offer_details'),
    path('my-offer/', MyOffers.as_view(), name='my_offer'),
    path('delete-<int:result_id>', delete_offer, name='delete_offer'),
    path('edit-<int:result_id>', edit_offer, name='edit_offer'),
    path('buy-item/', BuyingItem.as_view(), name='buy_item')
]