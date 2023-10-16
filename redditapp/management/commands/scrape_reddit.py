from django.core.management.base import BaseCommand
from django.conf import settings
import praw
from redditapp.models import Post
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = "Scrape data from the NationalServiceSG subreddit and keep only the latest top 100 hot posts."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting scraping...")

        # Establish a Reddit instance with PRAW (Python Reddit API Wrapper) using credentials from settings.
        reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )

        # Accessing the subreddit 'NationalServiceSG'.
        subreddit = reddit.subreddit('NationalServiceSG')

        # Delete the old posts in the database to maintain only the latest scraped posts.
        # to avoid duplication and keep the database up to date with the latest subreddit state.
        self.stdout.write("Deleting old posts...")
        Post.objects.all().delete()

        # Scrape the top 100 hot posts from the subreddit.
        for submission in subreddit.hot(limit=100):
            # Convert the submission timestamp to a timezone-aware datetime object.
            date_posted_dt = datetime.utcfromtimestamp(submission.created_utc)
            date_posted_dt = timezone.make_aware(date_posted_dt)

            # Create a new Post object and save it to the database.
            # Each Post includes the title, content, and the posting date.
            post = Post(title=submission.title, content=submission.selftext, date_posted=date_posted_dt)
            post.save()

        # Confirm the completion of the scraping process.
        self.stdout.write("Scraping completed.")
