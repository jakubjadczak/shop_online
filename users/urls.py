from django.urls import path
from .views import register_page, activate, user_login, user_logout

app_name = 'users'


urlpatterns = [
    path('register/', register_page, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
]