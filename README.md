# Reddit Analysis Project

This project seeks to understand the sentiments of Singaporeans serving National Service (NS) in Singapore, through the discussions in the r/NationalServiceSG subreddit. It is an initial MVP intended to assist policy makers and defence executives in decision-making and policies formulation. By scraping Reddit posts in the subreddit, a simple word frequency chart and word cloud is used to analysis and visualise their sentiments. This MVP drives the potential to deep dive into our National Service men’ sentiments through future analysis capabilities.

![Alt text](<Web Architecture.jpg>)

Actual Production Website: 
[http://sgjustino.pythonanywhere.com/]

## Setup

### Requirements

Ensure Python 3.8 or higher is installed on your system. Install the required libraries using:

```bash
pip install -r requirements.txt
```

### Database Migrations

Apply database migrations before starting the server. Execute the following command:

```bash
python manage.py migrate
```

### Scraping Command

Populate your database with the latest posts from the subreddit by running the custom scraping command:

```bash
python manage.py scrape_reddit
```
This command updates the database with the latest posts.

### Running the Server

Start the application by launching the Django development server:

```bash
python manage.py runserver
```
Access the web application by navigating to [http://localhost:8000/](http://localhost:8000/) in your web browser.

## Build and Run via Docker
```bash
docker build -t reddit_project .
```
Build up docker image
```bash
docker run -p 8000:8000 reddit_project
```
Run the Docker container and access the web application by navigating to [http://localhost:8000/](http://localhost:8000/) in your web browser.

Note: The static files are served through PythonAnywhere web server. Hence, I did not hard-code it in urls.py through Django development server's automatic static file. To see the images, go to the website linked below.

## Rubric Assessment

### Web application basic form, reporting
*Web App on [http://sgjustino.pythonanywhere.com/]
*Suggestion Form at the bottom of the page
*Reporting via Analysis Charts

### Data collection
*Praw Library is utilised as a reddit api wrapper to scrape data from the subreddit r/NationalServiceNS
/redditapp/management/commands/scrape_reddit.py

### Data analyzer
*Data Cleaning: The Natural Language Toolkit (NLTK) is used to clean, transform, and tokenize the raw post data, preparing it for further analysis.

*Sentiment Analysis: The Vader Sentiment Analysis tool is used to interpret posts and categorise them as positive, neutral, or negative.

*Word Frequency Chart: The NLTK's frequency distribution is used to visualize the most common terms in the posts based on word frequency.

*Word Cloud: A word cloud is generated with Matplotlib based on word frequency.

/redditapp/analysis.py

### Unit tests
```bash
python manage.py test
```
*Unit tests include test_analysis.py, test_models.py and test_views.py
/redditapp/tests/
![Alt text](<Test Results.jpg>)

### Data persistence any data store
*Data stored in SQLite db due to relative small and uncomplicated data
/db.sqlite3

### Rest collaboration internal or API endpoint
API endpoint: Reddit API for Data collection via PRAW wrapper
/redditapp/management/commands/scrape_reddit.py

### Product environment
PythonAnywhere virtualenv is used to host the web application.
Folder is also containerized via Docker although static images are wired for production on PythonAnywhere.

### Integration tests
```bash
python manage.py test
```
All tests are found in /redditapp/tests/
Integration tests is found in test_integration.py

### Using mock objects or any test doubles
```bash
python manage.py test
```
All tests are found in /redditapp/tests/
Mock objects are used in test_analysis.py

### CI/CD Integration
*Direct integration via Github Actions

### Production monitoring instrumenting
*Monitoring via PythonAnywhere Always-On Task running health.py
/redditapp/monitoring/health.py

### Event collaboration messaging
*Daily Scheduler for web scraping via PythonAnywhere Scheduled Task running scrape_reddit.py
*No need for per-user request as the hot topic posts in the subreddit will not fluctuate much below a 24-hour cycle.
/redditapp/management/commands/scrape_reddit.py