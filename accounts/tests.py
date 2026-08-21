from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import UserProfile

# Create your tests here.

User = get_user_model()

@override_settings(RATELIMIT_ENABLE=False)
class RegisterViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:register')

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_successful_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@citadel.ua',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_created_automatically_via_signal(self):
        data = {
            'username': 'signaluser',
            'email': 'signal@citadel.ua',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        self.client.post(self.url, data)
        user = User.objects.filter(username='signaluser').first()
        if user:
            self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_register_with_wrong_passwords(self):
        data = {
            'username': 'baduser',
            'email': 'bad@citadel.ua',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass456!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_authenticated_user_redirected_from_register(self):
        User.objects.create_user(username='existing', password='pass123')
        self.client.login(username='existing', password='pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@citadel.ua',
            password='testpass123',
        )
        UserProfile.objects.get_or_create(user=self.user)
        self.url = reverse('accounts:profile')

    def test_profile_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_profile_loads_when_logged_in(self):
        self.client.login(username='profileuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_update(self):
        self.client.login(username='profileuser', password='testpass123')
        data = {
            'username': 'profileuser',
            'email': 'updated@citadel.ua',
            'first_name': 'Артур',
            'last_name': 'Пендрагон',
            'address': 'вул. Лицарів, 1',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@citadel.ua')