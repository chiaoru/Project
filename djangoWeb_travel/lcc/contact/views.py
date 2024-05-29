from django.shortcuts import render

# Create your views here.
from .models import Message

def contact(request):
    
    if 'username' in request.POST:
        uname = request.POST['username']
        umail = request.POST['email']
        usub = request.POST['subject']
        ucontent = request.POST['content']
        
        
        # 將收到的資料新增到資料庫中的資料表
        obj = Message.objects.create(name=uname, email=umail, subject=usub, content=ucontent)
        
        obj.save()
        
        #標準的SQL語法為：
        
        
    return render(request,'contact.html')  

def about(request):
    
    return render(request, 'about.html')