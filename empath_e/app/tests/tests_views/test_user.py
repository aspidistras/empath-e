from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User


class UserViewsTestCase(TestCase):
    """Test app user views"""

    def setUp(self):
        self.user = User.objects.create_user(username='test', first_name='test', last_name='test',
                                            email='test@test.fr', password='test')
        self.client = Client()


    def test_login_page(self):
        """Check that login page returns status code 200"""

        response = self.client.get(reverse('app:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Check that logout page returns status code 200"""

        self.client.login(username='test', password='test')
        self.client.logout()

        response = self.client.get(reverse('app:logout'))
        self.assertEqual(response.status_code, 302)

    def test_account(self):
        """Check that personnal account page returns status code 200"""
        
        self.client.login(username='test', password='test')

        response = self.client.get(reverse('app:account'))
        self.assertEqual(response.status_code, 200)

    def test_create_account(self):
        """Check that create account page returns status code 200"""

        response = self.client.get(reverse('app:create_account'))
        self.assertEqual(response.status_code, 200)


