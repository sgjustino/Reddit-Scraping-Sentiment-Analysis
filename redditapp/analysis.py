import os
import nltk
import random
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from redditapp.models import Post
from nltk.sentiment import SentimentIntensityAnalyzer
from django.conf import settings

def download_nltk_datasets():
    """
    Download necessary NLTK datasets if they are not already present. For reviewers
    """
    datasets = {
        'punkt': 'tokenizers/punkt/english.pickle',
        'stopwords': 'corpora/stopwords',
        'vader_lexicon': 'sentiment/vader_lexicon.zip'
    }

    for dataset, path in datasets.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(dataset)

# Initialize necessary datasets for NLTK.
download_nltk_datasets()

def fetch_posts(limit=None):
    """
    Retrieve posts from database.
    """
    return Post.objects.all()[:limit] if limit else Post.objects.all()

def get_word_frequencies(posts):
    """
    Calculate frequency of each word in posts' content.
    """
    # Combine all posts into a single text.
    text = " ".join([post.content for post in posts])

    # Tokenize text into words.
    tokens = word_tokenize(text)

    # Remove non-alphabetic tokens and make all words lowercase.
    words = [word.lower() for word in tokens if word.isalpha()]

    # Filter out common stopwords (e.g., 'the', 'a', 'in').
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Count frequency of each word.
    return Counter(filtered_words)

def compute_sentiment(posts):
    """
    Compute overall sentiment of posts.
    """
    sia = SentimentIntensityAnalyzer()
    sentiments = [sia.polarity_scores(post.content)['compound'] for post in posts]

    if not sentiments:
        return "No posts to analyze"

    # Compute average sentiment.
    avg_sentiment = sum(sentiments) / len(sentiments)

    # Determine overall sentiment based on average score.
    if avg_sentiment >= 0.05:
        return "Positive"
    elif avg_sentiment <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def create_word_cloud(frequencies):
    """
    Create a word cloud image from word frequencies.
    """
    
    if not frequencies:
        return None

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies)

    # Define full file path
    img_path = os.path.join(settings.BASE_DIR, 'redditapp/static/redditapp/img/wordcloud.png')
    
    # Save the image
    wordcloud.to_file(img_path)

    # Return relative path
    return 'redditapp/img/wordcloud.png'

if __name__ == '__main__':
    # Fetch a limited number of posts for analysis.
    posts = fetch_posts(limit=100)

    # Get word frequencies from posts' content.
    frequencies = get_word_frequencies(posts)

    # Create a word cloud image.
    word_cloud_image_path = create_word_cloud(frequencies)

    # Print frequencies and overall sentiment of posts.
    print(frequencies)
    print(compute_sentiment(posts))

    # If script generated a word cloud, print path to image.
    if word_cloud_image_path:
        print(f"Word cloud saved at: {word_cloud_image_path}")
