from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from redditapp.models import Post, Suggestion
from redditapp.forms import SuggestionForm

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')  # Ensure 'dashboard' is the name of URL pattern.

    def test_dashboard_GET(self):
        # Test for a GET request to the dashboard view.
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)  # Check that the response is 200 OK.
        self.assertTemplateUsed(response, 'redditapp/dashboard.html')  # Ensure the correct template was used.

    def test_dashboard_no_posts(self):
        # Test the behavior of the dashboard when there are no posts.
        response = self.client.get(self.dashboard_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'No posts available for analysis.')

    def tearDown(self):
        # Clean-up test cases
        pass
