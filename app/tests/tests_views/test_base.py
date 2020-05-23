from django.test import TestCase
from django.urls import reverse
from django.core import mail

from app.models.resources import Disorder, Link


class BasicViewsTestCase(TestCase):
    """Test app basic views"""

    def setUp(self):
        self.disorder = Disorder.objects.create(name='test', details='test data', url_pattern='test')


    def test_index_page(self):
        """Check that index page returns status code 200"""

        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

    def test_contat_form(self):
        """Check that contact form is validated and email is send to admin"""

        response = self.client.post('/', {'email': 'test@test.fr', 'subject': 'test', 'message': 'test'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'Message suivant : \'test\' de la part de test@test.fr')
        self.assertEqual(mail.outbox[0].from_email, 'test@test.fr')
        self.assertEqual(mail.outbox[0].to, ['empath.e.oc@gmail.com'])
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


    def test_disorders_list_page(self):
        """Check that disorders list page returns status code 200 and displays disorders list"""

        response = self.client.get(reverse('app:disorders_list'))
        self.assertContains(response, 'test')
        self.assertEqual(response.status_code, 200)

    
    def test_disorder_details_page(self):
        """Check that disorder detail page returns status code 200 and displays disorder data"""

        response = self.client.get(reverse('app:disorder_details', args=[self.disorder.url_pattern]))
        url = reverse('app:disorder_details', args=[self.disorder.url_pattern])
        self.assertURLEqual('/disorder/' + self.disorder.url_pattern + '/', url)
        self.assertContains(response, 'test data')
        self.assertEqual(response.status_code, 200)
        

        



