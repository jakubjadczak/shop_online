from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = CustomUser.objects.create_user(
            username='user_test',
            password='test_Password1@',
            email='test@user.com'
        )

        self.test_user.is_active = True
        self.test_user.save()

    def test_register_get(self):
        response = self.client.get(reverse('users:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_post(self):
        response = self.client.post(reverse('users:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    # TODO test login
    '''
    def test_login_post(self):
        response = self.client.post(reverse('users:login'), {
            'username': self.test_user.username,
            'password': self.test_user.password

        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    '''

    def test_logout(self):
        response = self.client.post(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)

    '''
    def test_change_password_post(self):
        response = self.client.post(reverse('users:change_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_password.html')
    '''

    def test_reset_code_send_post(self):
        response = self.client.post(reverse('users:reset_password_send_code'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reset_password.html')

    def test_reset_code_send_get(self):
        response = self.client.get(reverse('users:reset_password_send_code'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_send_code.html')

    '''
    def test_reset_password_post(self):
        response = self.client.post(reverse('users:reset_password'), {
            'user_email': 'test@user.com'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reset_password.html')
    '''

    def test_reset_password_get(self):
        response = self.client.get(reverse('users:reset_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reset_password.html')