# Inside fetch_google_news.py
from django.core.management.base import BaseCommand
from NewsPaper.models import GoogleNewsArticle
from pygooglenews import GoogleNews
from django.utils.text import Truncator
from django.utils import timezone
from dateutil import parser

class Command(BaseCommand):
    help = 'Fetch news from Google News and store in the database'

    def handle(self, *args, **kwargs):
        # Instantiate GoogleNews
        gn = GoogleNews(lang='en', country='US')  # You can modify language and country based on your needs

        # Fetch top news related to politics
        politics_result = gn.search('politics', proxies=None, scraping_bee=None)
        politics_articles = politics_result['entries']
        self.save_to_database(politics_articles)

        # Fetch top world news
        world_result = gn.topic_headlines('world', proxies=None, scraping_bee=None)
        world_articles = world_result['entries']
        self.save_to_database(world_articles)

        self.stdout.write(self.style.SUCCESS('News from Google News successfully fetched and stored.'))

    def save_to_database(self, articles):
        for article in articles:
            # Ensure 'title' and 'link' are present in the article dictionary
            title = article.get('title', '')
            link = article.get('link', '')

            # Truncate title and link if needed
            truncated_title = Truncator(title).chars(300)
            truncated_link = Truncator(link).chars(200)

            # Ensure that the lengths are within an acceptable range
            if len(truncated_title) > 300:
                truncated_title = truncated_title[:300]
            if len(truncated_link) > 200:
                truncated_link = truncated_link[:200]

            # Parse the date string to a datetime object (aware)
            published_date_str = article.get('published', '')
            if published_date_str:
                try:
                    parsed_date = parser.parse(published_date_str)
                    if timezone.is_naive(parsed_date):
                        
                        published_date = timezone.make_aware(parsed_date)
                    else:
                        published_date = parsed_date
                except parser.ParserError:
                   
                    published_date = timezone.now()
            else:
                
                published_date = timezone.now()

            GoogleNewsArticle.objects.create(
                title=truncated_title,
                link=truncated_link,
                published_date=published_date,
            )
