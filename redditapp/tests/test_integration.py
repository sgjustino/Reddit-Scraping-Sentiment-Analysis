from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from redditapp.models import Post, Suggestion
from redditapp.forms import SuggestionForm
import os
from django.conf import settings

class FullStackIntegrationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a post with date_posted
        cls.post = Post.objects.create(
            title='Test Post', 
            content='Just a test post content.',
            date_posted=timezone.now()  # Add current date and time
        )


    def test_dashboard_view_integration(self):
        client = Client()

        # Load dashboard
        response = client.get(reverse('dashboard'))

        # Check page is rendered correctly and the status code = 200
        self.assertEqual(response.status_code, 200)

        # Check if the context contains the required keys
        self.assertIn('avg_sentiment', response.context)
        self.assertIn('image_path', response.context)
        self.assertIn('wordcloud_image_path', response.context)
        self.assertIn('suggestions', response.context)
        self.assertIsInstance(response.context['form'], SuggestionForm)

        # Check if images are generated
        if response.context['image_path']:
            self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'redditapp/static/', response.context['image_path'])))

        if response.context['wordcloud_image_path']:
            self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'redditapp/static/', response.context['wordcloud_image_path'])))

        # test the POST request, simulating a form submission.
        response_post = client.post(reverse('dashboard'), {'text': 'A new suggestion!'})

        # redirect (302) to the same 'dashboard' view.
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(Suggestion.objects.count(), 1)  # Check if a suggestion added

        # The suggestion text should match what was posted.
        suggestion = Suggestion.objects.first()
        self.assertEqual(suggestion.text, 'A new suggestion!')

        # check if new suggestion included
        response = client.get(reverse('dashboard'))
        self.assertContains(response, 'A new suggestion!')
