from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User, Group


class UserViewsTestCase(TestCase):
    """Test app user views"""

    def setUp(self):
        self.user = User.objects.create_user(username='test', first_name='test', last_name='test',
                                             email='test@test.fr', password='test')
        self.raise_awareness_group = Group.objects.create(name='Sensibiliser')
        self.raise_awareness_user = User.objects.create_user(username='test_awareness', first_name='test', last_name='test',
                                                             email='test.awareness@test.fr', password='test')
        self.raise_awareness_user.groups.add(self.raise_awareness_group)
        self.want_to_understand_group = Group.objects.create(name='Comprendre')
        self.want_to_understand_user = User.objects.create_user(username='test_understand', first_name='test', last_name='test',
                                                                email='test.understand@test.fr', password='test')
        self.want_to_understand_user.groups.add(self.want_to_understand_group)

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

    def test_access_account_raise_awareness(self):
        """Check that personnal account contains raise awareness user specific data"""

        self.client.login(username='test_awareness', password='test')
        response = self.client.get(reverse('app:account'))
        self.assertContains(response, '<a class="btn btn-primary" href="/">Je veux témoigner</a>')

    
    def test_access_account_want_to_understand(self):
        """Check that personnal account contains want to understand user specific data"""
            
        self.client.login(username='test_understand', password='test')
        response = self.client.get(reverse('app:account'))
        self.assertContains(response, '<a class="btn btn-primary" href="/">Créer une requếte</a>')
