from django.test import TestCase
from django.urls import reverse


class BasicViewsTestCase(TestCase):
    """Test app basic views"""

    def test_index_page(self):
        """Check that index page returns status code 200"""

        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

    def test_legal_notices_page(self):
        """Check that legal notices page returns status code 200"""

        response = self.client.get(reverse('app:legal_notices'))
        self.assertEqual(response.status_code, 200)

    def test_resources_page(self):
        """Check that ressources page returns status code 200"""

        response = self.client.get(reverse('app:resources'))
        self.assertEqual(response.status_code, 200)

    def test_testimonies_page(self):
        """Check that testimonies page returns status code 200"""

        response = self.client.get(reverse('app:testimonies'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """Check that about page returns status code 200"""

        response = self.client.get(reverse('app:about'))
        self.assertEqual(response.status_code, 200)

