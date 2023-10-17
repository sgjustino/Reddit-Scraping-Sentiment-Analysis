# Reddit Analysis Project

This project seeks to understand the sentiments of Singaporeans serving National Service (NS) in Singapore, through the discussions in the r/NationalServiceSG subreddit. It is an initial MVP intended to assist policy makers and defence executives in decision-making and policies formulation. By scraping Reddit posts in the subreddit, a simple word frequency chart and word cloud is used to analysis and visualise their sentiments. This MVP drives the potential to deep dive into our National Service men’ sentiments through future analysis capabilities.

![Alt text](<Web Architecture.jpg>)

## Requirements

Ensure Python 3.10 or higher is installed on your system. Install the required libraries using:

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

## CI/CD Integration

Direct integration via Github Actions

