from django.test import TestCase
from redditapp.models import Post, Suggestion
from django.utils import timezone

class PostModelTest(TestCase):
    def setUp(self):
        # Create a Post instance to use in tests
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test content',
            date_posted=timezone.now()
        )

    def test_post_creation(self):
        """
        Test to ensure that the Post model saves data as expected.
        """
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test content')
        self.assertIsInstance(self.post.date_posted, type(timezone.now()))

    def test_post_str(self):
        """
        Test the __str__ method, which should return the post title.
        """
        self.assertEqual(str(self.post), 'Test Post')

class SuggestionModelTest(TestCase):
    def setUp(self):
        # Create a Suggestion instance to use in tests
        self.suggestion = Suggestion.objects.create(
            text='This is a test suggestion'
        )

    def test_suggestion_creation(self):
        """
        Test to ensure that Suggestion model saves data as expected.
        """
        self.assertEqual(self.suggestion.text, 'This is a test suggestion')
        self.assertIsInstance(self.suggestion.created_at, type(timezone.now()))

    def test_suggestion_str(self):
        """
        Test the __str__ method, which should return the suggestion text.
        """
        self.assertEqual(str(self.suggestion), 'This is a test suggestion'[:50])
