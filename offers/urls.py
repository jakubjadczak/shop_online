from django.urls import path
from .views import AddOffer

app_name = 'offer'

urlpatterns = [
    path('add-offer/', AddOffer.as_view(), name='add_offer'),
]