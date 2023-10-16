import os
import nltk
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as patches
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from redditapp.models import Post
from nltk.sentiment import SentimentIntensityAnalyzer
from django.conf import settings

def download_nltk_datasets():
    """
    Download necessary NLTK datasets if they are not already present.
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

# Initialize the necessary datasets for NLTK.
download_nltk_datasets()

def fetch_posts(limit=None):
    """
    Retrieve posts from the database.

    :param limit: The maximum number of posts to retrieve.
    :return: A queryset of posts.
    """
    return Post.objects.all()[:limit] if limit else Post.objects.all()

def get_word_frequencies(posts):
    """
    Calculate the frequency of each word in the posts' content.

    :param posts: A queryset of posts.
    :return: A Counter object with word frequencies.
    """
    # Combine all posts into a single text.
    text = " ".join([post.content for post in posts])

    # Tokenize the text into words.
    tokens = word_tokenize(text)

    # Remove non-alphabetic tokens and make all words lowercase.
    words = [word.lower() for word in tokens if word.isalpha()]

    # Filter out common stopwords (e.g., 'the', 'a', 'in').
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Count the frequency of each word.
    return Counter(filtered_words)

def compute_sentiment(posts):
    """
    Compute the overall sentiment of the posts.

    :param posts: A queryset of posts.
    :return: A string indicating the overall sentiment.
    """
    sia = SentimentIntensityAnalyzer()
    sentiments = [sia.polarity_scores(post.content)['compound'] for post in posts]

    if not sentiments:
        return "No posts to analyze"

    # Compute the average sentiment.
    avg_sentiment = sum(sentiments) / len(sentiments)

    # Determine the overall sentiment based on the average score.
    if avg_sentiment >= 0.05:
        return "Positive"
    elif avg_sentiment <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def create_word_cloud(frequencies):
    """
    Create a word cloud image from word frequencies.

    :param frequencies: A Counter object with word frequencies.
    :return: The relative path to the saved word cloud image.
    """
    if not frequencies:
        return None

    # Get the top 100 words.
    top_frequencies = dict(frequencies.most_common(100))

    # Calculate the maximum frequency.
    max_freq = max(top_frequencies.values())

    # Set the size of the plot.
    plt.figure(figsize=(10, 6))

    # Define colors to use in the word cloud.
    colors = list(mcolors.TABLEAU_COLORS.values())

    # Ensure there are enough colors by repeating the list if necessary.
    while len(colors) < len(top_frequencies):
        colors.extend(colors)

    # Define the scale factor for font sizes.
    scale_factor = 60  # Making fonts three times bigger

    # Define margins and text area within the plot.
    x_margin = 50  # Increased margin size to ensure words do not spill over.
    y_margin = 50  # Same here.
    x_range = 600  # Reduced range so words appear more centered.
    y_range = 300  # Same here.

    # Randomly scatter words across the plot with sizes and colors based on their frequency.
    for (word, freq), color in zip(top_frequencies.items(), colors):
        # Compute the size of the text.
        fontsize = freq * scale_factor / max_freq
        # Avoid placing text too close to the borders by considering the text size.
        x_random = random.randint(x_margin, x_margin + x_range - int(fontsize))
        y_random = random.randint(y_margin, y_margin + y_range - int(fontsize))
        
        plt.text(
            x_random,
            y_random,
            word,
            fontsize=fontsize,
            ha='center',
            va='center',
            color=color
        )

    # Create a Rectangle patch for the border.
    border = patches.Rectangle((x_margin, y_margin), x_range, y_range, linewidth=2, edgecolor='black', facecolor='none')

    # Add the patch representing the border to the Axes.
    plt.gca().add_patch(border)

    plt.xlim(0, x_margin + x_range + x_margin)  # Set the horizontal limits to the width of the border.
    plt.ylim(0, y_margin + y_range + y_margin)  # Set the vertical limits to the height of the border.
    plt.axis("off")
    plt.tight_layout()

    # Define the full file path.
    img_path = os.path.join(settings.BASE_DIR, 'redditapp/static/redditapp/img/wordcloud.png')
    
    # Save the image.
    plt.savefig(img_path, format="png", dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure.

    # Return the relative path.
    return 'redditapp/img/wordcloud.png'

if __name__ == '__main__':
    # Fetch a limited number of posts for analysis.
    posts = fetch_posts(limit=100)

    # Get the word frequencies from the posts' content.
    frequencies = get_word_frequencies(posts)

    # Create a word cloud image.
    word_cloud_image_path = create_word_cloud(frequencies)

    # Print the frequencies and the overall sentiment of the posts.
    print(frequencies)
    print(compute_sentiment(posts))

    # If the script generated a word cloud, print the path to the image.
    if word_cloud_image_path:
        print(f"Word cloud saved at: {word_cloud_image_path}")
