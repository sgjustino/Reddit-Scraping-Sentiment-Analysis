from django.core.management.base import BaseCommand
from django.conf import settings
import praw
from redditapp.models import Post
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = "Scrape data from NationalServiceSG subreddit and keep only latest top 100 hot posts."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting scraping...")

        # Establish a Reddit instance with PRAW (Python Reddit API Wrapper) using credentials from settings.
        reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )

        # Accessing subreddit 'NationalServiceSG'.
        subreddit = reddit.subreddit('NationalServiceSG')

        # Delete old posts in database to maintain only latest scraped posts.
        # Avoid duplication and keep database up to date with  latest subreddit state.
        self.stdout.write("Deleting old posts...")
        Post.objects.all().delete()

        # Scrape top 100 hot posts from subreddit.
        for submission in subreddit.hot(limit=100):
            # Convert submission timestamp to a timezone-aware datetime object.
            date_posted_dt = datetime.utcfromtimestamp(submission.created_utc)
            date_posted_dt = timezone.make_aware(date_posted_dt)

            # Create a new Post object and save it to database.
            # Each Post includes title, content, and posting date.
            post = Post(title=submission.title, content=submission.selftext, date_posted=date_posted_dt)
            post.save()

        # Confirm completion of scraping process.
        self.stdout.write("Scraping completed.")
