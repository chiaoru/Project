from django.shortcuts import render

# Create your views here.
import hashlib
from .models import Customer
from django.http import HttpResponseRedirect, HttpResponse

def login(request):
    msg = ""
    if "email" in request.POST:
        email = request.POST['email']
        pwd = request.POST['password']
        pwd = hashlib.sha3_256(pwd.encode('utf-8')).hexdigest()
        obj = Customer.objects.filter(email=email, password=pwd).count()
        if obj > 0:
            request.session['cusEmail'] = email
            request.session['isAlive'] = True
            request.session['lcc'] = 'good'
            
            response = HttpResponseRedirect('/')
            response.set_cookie('UEmail', email, max_age=1200)
            return response
        
        else:
            msg = "帳號或密碼錯誤！"
            return render(request, 'login.html', locals())
        
    else:
        return render(request, 'login.html', locals())

def logout(request):
    # 登出後刪除session
    del request.session['cusEmail']
    del request.session['isAlive']
    del request.session['lcc']
    request.session.clear()
    response = HttpResponseRedirect('/')
    response.delete_cookie('UEmail')
    return response

def register(request):
    msg = ""
    if "uEmail" in request.POST:
        uName = request.POST['uName']
        uEmail = request.POST['uEmail']
        pwd = request.POST['pwd']
        sex = request.POST['sex']
        birthday = request.POST['birthday']
        mobile = request.POST['mobile']
        address = request.POST['address']
        
        pwd = hashlib.sha3_256(pwd.encode('utf-8')).hexdigest()
        
        obj = Customer.objects.filter(email=uEmail).count()
        if obj == 0:
            Customer.objects.create(name=uName, sex=sex, birthday=birthday, email=uEmail, mobile=mobile, address=address, password=pwd)
            
            msg = "註冊成功！"
            
        else:
            msg = "Email重複，請更新一個！"
    
    return render(request, 'register.html', locals())

def ChangePassword(request):
    if 'cusEmail' in request.session and 'lcc' in request.session:
        msg = ''
        
        if 'oldPwd' in request.POST: # 當舊密碼相同才能更改密碼
            oldPwd = request.POST['oldPwd']
            oldPwd = hashlib.sha3_256(oldPwd.encode('utf-8')).hexdigest()
            
            newPwd = request.POST['newPwd']
            newPwd = hashlib.sha3_256(newPwd.encode('utf-8')).hexdigest()
            
            email = request.session['cusEmail']
            obj = Customer.objects.filter(email=email, password=oldPwd).count()
            if obj > 0:
                user = Customer.objects.get(email=email) # 因為一定有此使用者，所以用get
                user.password = newPwd
                user.save()
                msg = '密碼變更成功！'
            else:
                msg = '就密碼錯誤，請重新輸入！'
                
        return render(request, 'updatepassword.html', locals())
    else:
        # 當未登入時，即跳轉到登入頁
        return HttpResponseRedirect('/login')