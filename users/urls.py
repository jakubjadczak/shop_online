from django.urls import path
from .views import register_page, activate

app_name = 'users'


urlpatterns = [
    path('register/', register_page, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]