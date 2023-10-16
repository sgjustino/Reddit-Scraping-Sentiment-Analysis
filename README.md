# Reddit Analysis Project

This Django-based application scrapes and analyzes data from a specific subreddit, presenting insights through textual analysis and visual representation.

## Requirements

Ensure Python 3.7 or higher is installed on your system. Install the required libraries using:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. Copy the `.env.sample` file in the project's root directory, and rename it to `.env`.
2. Update the variables within the `.env` file with your specific Reddit API credentials:

```plaintext
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## Database Migrations

Apply database migrations before starting the server. Execute the following command:

```bash
python manage.py migrate
```

## Scraping Command

Populate your database with the latest posts from the subreddit by running the custom scraping command:

```bash
python manage.py scrape_reddit
```
This command updates the database with the latest posts.

## Running the Server

Start the application by launching the Django development server:

```bash
python manage.py runserver
```

Access the web application by navigating to [http://localhost:8000/](http://localhost:8000/) in your web browser.
```
