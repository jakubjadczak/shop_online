from django.urls import path
from .views import register_page

app_name = 'users'


urlpatterns = [
    path('register/', register_page, name='register')
]