# news_app/management/commands/fetch_newsapi.py
from django.core.management.base import BaseCommand
from NewsPaper.models import NewsApiArticle
from datetime import datetime

import requests

class Command(BaseCommand):
    help = 'Fetch and store news from News API'

    def handle(self, *args, **options):
        # Replace 'your_api_key' with your actual News API key
        api_key = 'c5427eee7a4844a18aac4fce7bde011b'
        base_url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'pageSize': 5,  # Limiting to 50 articles
            'country': 'us',  # Change country as needed
        }

        # Make a GET request to News API
        response = requests.get(base_url, params=params)
        data = response.json()

        # Store news in the database
        for article in data.get('articles', []):
            title = article.get('title')
            url = article.get('url')
            published_at = datetime.strptime(article.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ')
            description = article.get('description', '')

            # Check if description is present, if not, provide a default value
            if not description:
                description = "No description available"

            NewsApiArticle.objects.create(
                title=title,
                url=url,
                published_at=published_at,
                description=description,
            )

        # Output a success message
        self.stdout.write(self.style.SUCCESS('News from News API successfully fetched and stored.'))
