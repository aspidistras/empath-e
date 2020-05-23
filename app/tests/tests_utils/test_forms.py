from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User, Group
from app.forms.user import UserForm
from app.forms.login import LoginForm
from app.forms.testimony import TestimonyForm
from app.forms.request import RequestForm
from app.models.resources import Disorder


class UserFormsTestCase(TestCase):
    """Test user related forms"""

    def setUp(self):
        self.test_group = Group.objects.create(name='test')
        self.disorder = Disorder.objects.create(name="test", details="test", url_pattern="test")

    def test_login_form(self):
        """Check that login form is valid"""

        form_data = {'username': 'test', 'password': 'test'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_account_creation_form(self):
        """Check that account creation form is valid"""

        form_data = {'username': 'test', 'password': 'test', 'first_name': 'test', 'last_name': 'test', 'email': 'test@test.fr', 'groups': self.test_group.name}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_testimony_form(self):
        """Check that testimoy creation form data is valid"""

        form_data = {'content': 'test', 'disorders': self.disorder}
        form = TestimonyForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_request_form(self):
        """Check that request creation form data is valid"""

        form_data = {'message': 'test', 'disorders': self.disorder}
        form = RequestForm(data=form_data)
        assert form.is_valid(), form.errors