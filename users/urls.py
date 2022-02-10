from django.urls import path
from .views import register_page, activate, user_login, user_logout, my_account_page, change_password,\
    ResetPasswordSendCode, ResetPassword

app_name = 'users'


urlpatterns = [
    path('register/', register_page, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('my_account/', my_account_page, name='my_account'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password_code/', ResetPasswordSendCode.as_view(), name='reset_password_send_code'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password')
]