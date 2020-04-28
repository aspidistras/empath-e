from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User, Group

from app.models.request import Request
from app.models.resources import Disorder
from app.models.testimony import Testimony
from app.forms.request import RequestForm
from app.forms.testimony import TestimonyForm


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

        self.disorder = Disorder.objects.create(name="test", details="test", url_pattern="test")

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
        self.assertContains(response, '<a class="btn btn-primary" href="/testify/">Je veux témoigner</a>')

    
    def test_access_account_want_to_understand(self):
        """Check that personnal account contains want to understand user specific data"""
            
        self.client.login(username='test_understand', password='test')
        response = self.client.get(reverse('app:account'))
        self.assertContains(response, '<a class="btn btn-primary" href="/request/">Créer une requếte</a>')


    def test_login_view(self):
        """Check that login form is validated and user is logged in"""
        
        response = self.client.post('/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, '/account/')

    
    def test_account_creation_view(self):
        """Check that account creation form is validated, new user is added to database and is redirected to thanks page"""

        user_count = len(User.objects.all())
        response = self.client.post('/new-user/', {'username': 'new', 'password': 'new', 'email': 'new@test.fr', 'first_name': 'new', 'last_name': 'new', 'groups': self.raise_awareness_group}, follow=True)
        new_user_count = len(User.objects.all())
        self.assertEqual(user_count + 1, new_user_count)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/rules/')


    def test_rules_view(self):
        """Check that thanks for creating an account and community rules page returns status code 200"""

        response = self.client.get(reverse('app:rules'))
        self.assertEqual(response.status_code, 200)


    def test_request_form(self):
        """Check that request creation form data is valid"""

        form_data = {'message': 'test', 'disorders': self.disorder}
        form = RequestForm(data=form_data)
        assert form.is_valid(), form.errors


    def test_new_request_view(self):
        """Check that request creation form is validated, new request is added to database and user is redirected to his account"""

        self.client.login(username='test_understand', password='test')

        response = self.client.get(reverse('app:request'))
        self.assertEqual(response.status_code, 200)

        request_count = len(Request.objects.all())
        response = self.client.post('/request/', {'message': 'test', 'disorders': self.disorder}, follow=True)
        new_request_count = len(Request.objects.all())

        self.assertEqual(Request.objects.get(pk=1).user, self.want_to_understand_user)
        self.assertEqual(request_count + 1, new_request_count)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/account/')

    
    def test_testimony_form(self):
        """Check that testimoy creation form data is valid"""

        form_data = {'content': 'test', 'disorders': self.disorder}
        form = TestimonyForm(data=form_data)
        assert form.is_valid(), form.errors

    
    def test_new_testimony_view(self):
        self.client.login(username='test_awareness', password='test')

        response = self.client.get(reverse('app:testify'))
        self.assertEqual(response.status_code, 200)

        testimony_count = len(Testimony.objects.all())
        response = self.client.post('/testify/', {'content': 'test', 'disorders': self.disorder}, follow=True)
        new_testimony_count = len(Testimony.objects.all())

        self.assertEqual(Testimony.objects.get(pk=1).user, self.raise_awareness_user)
        self.assertEqual(testimony_count + 1, new_testimony_count)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/account/')

        



    
