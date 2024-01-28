# news_app/models.py
from django.db import models

class GoogleNewsArticle(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    published_date = models.DateTimeField()
    CATEGORY_CHOICES = [
        ('politics', 'Politics'),
        ('world', 'World'),]

  


class NewsApiArticle(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    published_at = models.DateTimeField()
    description = models.TextField() 

    def __str__(self):
        return self.title
