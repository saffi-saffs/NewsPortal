from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from pygooglenews import GoogleNews

def News(request):
   
    gn = GoogleNews(lang='en', country='US')


    top = gn.top_news()
    top_entries = top['entries']


    entry_details = []

  
    for idx, entry in enumerate(top_entries, start=1):
        entry_detail = {
            'index': idx,
            'title': entry['title'],
            'published_date': entry['published'],
            'source': entry['source'],
            'news_summary': entry['summary'],
            'sub_articles': entry['sub_articles'],
        }
        entry_details.append(entry_detail)

   
    paginator = Paginator(entry_details, 5)  
    page = request.GET.get('page')

    try:
        entry_details = paginator.page(page)
    except PageNotAnInteger:
     
        entry_details = paginator.page(1)
    except EmptyPage:
       
        entry_details = paginator.page(paginator.num_pages)

 
    context = {'entry_details': entry_details}

  
    return render(request, "NewsPaper/newsindex.html", context)


