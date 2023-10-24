from unittest import TestCase, mock
from collections import Counter
from redditapp.analysis import get_word_frequencies, compute_sentiment, create_word_cloud

class AnalysisTestCase(TestCase):
    def setUp(self):
        pass

    @mock.patch('redditapp.analysis.Post')
    def test_get_word_frequencies(self, MockPost):
        # Setting up mock objects for testing
        mock_post = mock.Mock()
        mock_post.content = "test content with some common words"
        MockPost.objects.all.return_value = [mock_post]

        # Call function with mock object
        result = get_word_frequencies(MockPost.objects.all())

        # Verify function behavior with assertions
        expected_result = Counter(["test", "content", "common", "words"])  #no filtering for MVP yet
        self.assertEqual(result, expected_result)

    @mock.patch('redditapp.analysis.SentimentIntensityAnalyzer')
    @mock.patch('redditapp.analysis.Post')
    def test_compute_sentiment(self, MockPost, MockAnalyzer):
        # Setting up mock objects for testing
        mock_post = mock.Mock()
        mock_post.content = "test content"
        MockPost.objects.all.return_value = [mock_post]

        mock_analyzer_instance = MockAnalyzer.return_value
        mock_analyzer_instance.polarity_scores.return_value = {'compound': 0.5}

        # Call function with mock object
        result = compute_sentiment(MockPost.objects.all())

        # Verify function behavior with assertions
        self.assertEqual(result, "Positive")

    def tearDown(self):
        # Deinitialize testing context to cleanup after tests ran.
        pass
