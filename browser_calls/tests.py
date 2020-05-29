from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

# Create your tests here.

 
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from model_mommy import mommy


class GetTokenTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.raise_awareness_group = Group.objects.create(name='Sensibiliser')
        self.raise_awareness_user = User.objects.create_user(username='test_awareness', first_name='test', last_name='test',
                                                             email='test.awareness@test.fr', password='test')
        self.raise_awareness_user.groups.add(self.raise_awareness_group)

    def test_get_token_unauthenticated(self):
        # Arrange
        mock_capability = MagicMock()
        mock_capability.to_jwt.return_value = b'abc123'
        
        self.client.login(username='test_awareness', password='test')

        # Act
        with patch(
            'browser_calls.views.ClientCapabilityToken',
            return_value=mock_capability,
        ):
            response = self.client.get(reverse('browser_calls:token'))

        # Assert
        # Make sure our mock_capability object was called with the right
        # arguments and that the view returned the correct response
        self.assertTrue(mock_capability.allow_client_outgoing.called)
        mock_capability.allow_client_incoming.assert_called_once_with(
            'awareness_user'
        )
        self.assertTrue(mock_capability.to_jwt.called)

        self.assertEqual(response.content, b'{"token": "abc123"}')

    def test_get_token_authenticated(self):
        # Arrange
        mock_capability = MagicMock()
        mock_capability.to_jwt.return_value = b'foo123'

        self.client.login(username='test_awareness', password='test')

        # Act
        with patch(
            'browser_calls.views.ClientCapabilityToken',
            return_value=mock_capability,
        ) as mock:
            response = self.client.get(
                reverse('browser_calls:token'), {'forPage': reverse('app:user_requests_list')}
            )

        # Assert
        self.assertTrue(mock_capability.allow_client_outgoing.called)
        mock_capability.allow_client_incoming.assert_called_once_with(
            'awareness_user'
        )
        self.assertTrue(mock_capability.to_jwt.called)

        self.assertEqual(response.content, b'{"token": "foo123"}')


class CallTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.raise_awareness_group = Group.objects.create(name='Sensibiliser')
        self.raise_awareness_user = User.objects.create_user(username='test_awareness', first_name='test', last_name='test',
                                                             email='test.awareness@test.fr', password='test')
        self.raise_awareness_user.groups.add(self.raise_awareness_group)

    def test_call_support(self):
        self.client.login(username='test_awareness', password='test')
        # Act
        response = self.client.post(reverse('browser_calls:call'))

        # Assert
        self.assertIn('<Client>understand_user</Client>', str(response.content))