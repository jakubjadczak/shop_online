from django.urls import path
from .views import AddOffer, AddPhotos, DisplayOffer

app_name = 'offer'

urlpatterns = [
    path('add-offer/', AddOffer.as_view(), name='add_offer'),
    path('add-photos/', AddPhotos.as_view(), name='add_photos'),
    path('see-offer/', DisplayOffer.as_view(), name='see_offer'),
]