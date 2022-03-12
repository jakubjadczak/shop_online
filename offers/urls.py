from django.urls import path
from .views import AddOffer, AddPhotos

app_name = 'offer'

urlpatterns = [
    path('add-offer/', AddOffer.as_view(), name='add_offer'),
    path('add-photos/', AddPhotos.as_view(), name='add_photos')
]