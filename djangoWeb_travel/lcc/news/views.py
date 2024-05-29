from django.shortcuts import render

# Create your views here.

from .models import travelNews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def news(request):
    
    platform = ''
    
    if 'platform' in request.GET:
        
        platform = request.GET['platform']
        
        
        if (platform == "三立新聞"):
            allnews = travelNews.objects.filter(platform="三立新聞").order_by('createDate')
            
        elif (platform == 'TVBS'):
            allnews = travelNews.objects.filter(platform='TVBS').order_by('createDate')
            
        elif (platform == '東森新聞'):
            allnews = travelNews.objects.filter(platform='東森新聞').order_by('createDate')
        
        elif (platform == 'SwissInfo'):
            allnews = travelNews.objects.filter(platform='SwissInfo').order_by('createDate')
          
        else:
            allnews = travelNews.objects.all().order_by('-createDate')
            
    else:
        allnews = travelNews.objects.all().order_by('-createDate')
    
    paginator = Paginator(allnews, 10)
    page = request.GET.get('page')
    
    try:
        allnews = paginator.page(page)
    except PageNotAnInteger:
        allnews = paginator.page(1)
    except EmptyPage:
        allnews = paginator.page(paginator.num_pages)
        
    return render(request, 'news.html', locals())