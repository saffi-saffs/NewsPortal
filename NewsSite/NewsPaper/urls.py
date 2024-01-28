from django.urls import path,include
from . import views
from .views import News, NewsAPI
from .views import News, google_news_database
urlpatterns=[path("",views.News,name="news"),   path('google-news-database/', google_news_database, name='googlenews'),
    path('news-api/', NewsAPI, name='news_api'),]