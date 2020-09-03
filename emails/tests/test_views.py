from django.test import TestCase, Client
from emails.models import Email, Category
from django.urls import reverse
from django.contrib.auth.models import User

class IndexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        test_user1.save()

    def test_user_logged_in(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'test_user1')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/accounts/login/?next=/emails/')

    def test_index_page_if_logged_in(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'emails/index.html')

    def test_num_emails_in_response_context(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertTrue('num_emails' in response.context)
        self.assertTrue('num_emailtranslations' in response.context)