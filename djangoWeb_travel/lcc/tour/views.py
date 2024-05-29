from django.shortcuts import render

# Create your views here.
from .models import Travel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def tours(request):
        
    tour = ''
    if "tour" in request.GET:
        
        t = request.GET['tour']
        #先篩選地區
        if (t == "全區"):
            alltours = Travel.objects.all().order_by('-createDate')
        elif (t == "日本"):
            alltours = Travel.objects.filter(area__icontains=t).order_by('-createDate')
        elif (t == "韓國"):
            alltours = Travel.objects.filter(area__icontains=t).order_by('-createDate')
        elif (t == "泰國"):
            alltours = Travel.objects.filter(area__icontains=t).order_by('-createDate')
        elif (t == "歐洲"):
            alltours = Travel.objects.filter(area__icontains=t).order_by('-createDate')
        elif (t == "馬新"):
            alltours = Travel.objects.filter(area__icontains='馬來西亞/新加坡').order_by('-createDate')
        elif (t == "紐澳"):
            alltours = Travel.objects.filter(area__icontains='紐西蘭/澳洲').order_by('-createDate')
        elif (t == "中東"):
            alltours = Travel.objects.filter(area__icontains=t).order_by('-createDate')
            
        #在篩選旅遊平台
        elif (t == "全部"):
            alltours = Travel.objects.all().order_by('-createDate')
        elif (t == "東南旅遊"):
            alltours = Travel.objects.filter(platform__icontains=t).order_by('-createDate')
        elif (t == "易遊網"):
            alltours = Travel.objects.filter(platform__icontains=t).order_by('-createDate')
        elif (t == "東森旅遊"):
            alltours = Travel.objects.filter(platform__icontains=t).order_by('-createDate')
        
        
        #最後篩選關鍵字
        elif (len(t) > 0):
            alltours = Travel.objects.filter(title__icontains=t).order_by('-createDate')
        else:
            alltours = Travel.objects.all().order_by('-id') 
    else:
        alltours = Travel.objects.all().order_by('-id') 
    # 表示所有的資料all()由大到小排序order_by('-id')
    # order_by 排序 id 是欄位名稱
    # order_by('id') 依 id 做遞增
    # order_by('-id') 依 id 做遞減
        
    paginator = Paginator(alltours,9)
    page = request.GET.get('page')
    try:
        alltours = paginator.page(page)
    
    except PageNotAnInteger:
        alltours = paginator.page(1)
        
    except EmptyPage:
        alltours = paginator.page(paginator.num_pages)

    return render(request,'tour.html',locals())
    # locals() 將函式 tour 中的變數整個帶過去給 tour.html