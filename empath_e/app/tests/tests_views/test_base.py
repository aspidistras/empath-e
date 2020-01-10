from django.test import TestCase
from django.urls import reverse


class BasicViewsTestCase(TestCase):
    """Test app basic views"""

    def test_index_page(self):
        """Check that index page returns status code 200"""

        # get response
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

    def test_legal_notices_page(self):
        """Check that legal notices page returns status code 200"""

        # get response
        response = self.client.get(reverse('app:legal_notices'))
        self.assertEqual(response.status_code, 200)
