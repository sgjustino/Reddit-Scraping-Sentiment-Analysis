import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .models import Post, Suggestion
from .analysis import get_word_frequencies, compute_sentiment, create_word_cloud
from .forms import SuggestionForm

def plot_word_frequencies(frequencies, top_n=20):
    """
    Plot most frequent words from posts.
    """
    # Return if no word frequencies are provided.
    if not frequencies:
        return None

    # Prepare data for plotting.
    most_common = frequencies.most_common(min(len(frequencies), top_n))
    words, counts = zip(*most_common)

    # Create horizontal bar plot.
    plt.figure(figsize=(15, 10))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Counts')
    plt.title('Top 20 Most Common Words in r/NationalServiceSG')
    plt.gca().invert_yaxis()

    # Save plot as an image file.
    img_path = os.path.join(settings.BASE_DIR, 'redditapp/static/redditapp/img/word_freq.png')
    plt.savefig(img_path)
    plt.close()

    return 'redditapp/img/word_freq.png'

def dashboard_view(request):
    """
    Handle logic for dashboard view.
    """
    # Fetch all posts from database.
    posts = Post.objects.all()

    # Inform user if no posts are available.
    if not posts:
        messages.info(request, 'No posts available for analysis.')
        return render(request, 'redditapp/dashboard.html')

    # Analyze word frequencies in posts' content.
    frequencies = get_word_frequencies(posts)

    # Attempt to generate visual representations of data.
    try:
        image_path = plot_word_frequencies(frequencies)
        wordcloud_image_path = create_word_cloud(frequencies)
    except Exception as e:
        # Handle any errors during generation.
        messages.error(request, f'An error occurred during analysis: {e}')
        image_path = None
        wordcloud_image_path = None

    # Verify existence of generated images.
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'redditapp/static/', image_path or '')):
        image_path = None
        messages.info(request, 'Not enough data to generate frequency plot.')

    if not os.path.exists(os.path.join(settings.BASE_DIR, 'redditapp/static/', wordcloud_image_path or '')):
        wordcloud_image_path = None
        messages.info(request, 'Not enough data to generate word cloud.')

    # Compute average sentiment of the posts.
    avg_sentiment = compute_sentiment(posts)

    # Handle the suggestion form submission.
    if request.method == 'POST':
        suggestion_form = SuggestionForm(request.POST)
        if suggestion_form.is_valid():
            suggestion_form.save()
            messages.success(request, 'Thank you for your suggestion!')
            return redirect('dashboard')  # Redirecting to dashboard view.
    else:
        suggestion_form = SuggestionForm()

    # Retrieve all suggestions for display.
    suggestions = Suggestion.objects.all()

    # Prepare the context for rendering the template.
    context = {
        'avg_sentiment': avg_sentiment,
        'image_path': image_path,  # Path for the word frequency chart.
        'wordcloud_image_path': wordcloud_image_path,  # Path for the word cloud image.
        'suggestions': suggestions,  # User suggestions.
        'form': suggestion_form,  # Suggestion form.
    }

    # Render dashboard with the prepared context.
    return render(request, 'redditapp/dashboard.html', context)
