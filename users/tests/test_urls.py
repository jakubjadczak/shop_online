from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
    RegisterPage, activate,
    user_login, user_logout,
    my_account_page, change_password,
    ResetPasswordSendCode, ResetPassword
)


class TestUrls(SimpleTestCase):

    def test_register(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func.view_class, RegisterPage)

    def test_user_login(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, user_login)

    def test_user_logout(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, user_logout)

    def test_my_account(self):
        url = reverse('users:my_account')
        self.assertEqual(resolve(url).func, my_account_page)

    def test_change_password(self):
        url = reverse('users:change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_reset_password_send_code(self):
        url = reverse('users:reset_password_send_code')
        self.assertEqual(resolve(url).func.view_class, ResetPasswordSendCode)

    def test_reset_password(self):
        url = reverse('users:reset_password')
        self.assertEqual(resolve(url).func.view_class, ResetPassword)