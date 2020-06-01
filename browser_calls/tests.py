"""Browser calls with Twilio related tests"""


from unittest.mock import MagicMock, patch

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class GetTokenTest(TestCase):
    """Test getting auth token"""

    def setUp(self):
        self.client = Client()
        self.raise_awareness_group = Group.objects.create(name='Sensibiliser')
        self.raise_awareness_user = User.objects.create_user(username='test_awareness',
                                                             first_name='test', last_name='test',
                                                             email='test.awareness@test.fr',
                                                             password='test')
        self.raise_awareness_user.groups.add(self.raise_awareness_group)

    def test_get_token_authenticated(self):
        """Get token as logged in user test"""
        # Arrange
        mock_capability = MagicMock()
        mock_capability.to_jwt.return_value = b'foo123'

        self.client.login(username='test_awareness', password='test')

        # Act
        with patch('browser_calls.views.ClientCapabilityToken',
                   return_value=mock_capability,
        ) as mock:
            response = self.client.get(
                reverse('browser_calls:token'),
                {'forPage': reverse('app:user_requests_list')}
            )

        # Assert
        self.assertTrue(mock_capability.allow_client_outgoing.called)
        mock_capability.allow_client_incoming.assert_called_once_with(
            'awareness_user'
        )
        self.assertTrue(mock_capability.to_jwt.called)

        self.assertEqual(response.content, b'{"token": "foo123"}')


class CallTest(TestCase):
    """Test call"""

    def setUp(self):
        self.client = Client()
        self.raise_awareness_group = Group.objects.create(name='Sensibiliser')
        self.raise_awareness_user = User.objects.create_user(username='test_awareness',
                                                             first_name='test', last_name='test',
                                                             email='test.awareness@test.fr',
                                                             password='test')
        self.raise_awareness_user.groups.add(self.raise_awareness_group)

    def test_call_user(self):
        """Test call user"""
        self.client.login(username='test_awareness', password='test')
        # Act
        response = self.client.post(reverse('browser_calls:call'))

        # Assert
        self.assertIn('<Client>understand_user</Client>', str(response.content))
