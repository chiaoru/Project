from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponseRedirect
from cart import models
from tour.models import Travel

import importlib.util

import os
from django.utils.html import format_html

# 抓取目前預設目錄位置 (lcc/lcc/setting.py中有寫)
basedir = os.path.dirname(__file__)
file = os.path.join(basedir, 'ecpay_payment_sdk.py')

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime


# 全域變數
cartlist = list()
guestname = ''
guestphone = ''
guestaddress = ''
guestemail = ''
orderTotal = 0
goodsTitle = list() # 放入購物車商品品項

#購物車
def cart(request):
    
    global cartlist
    goodslist = cartlist
    total = 0
    
    for unit in cartlist:
        total += int(unit[3])
        
    if total >= 10000:
        grandtotal = total     
    else:
        grandtotal = total + 200
        
    if len(goodslist) == 0:
        empty = 1
    else:
        empty = 0
        
    return render(request, 'cart.html', locals())
        

#商品加到購物車
def addtocart(request, ctype=None, toursid=None):
    global cartlist #全域變數
    
    if ctype == 'add':
        tours = Travel.objects.filter(id=toursid).count()
        if tours > 0:
            tours = Travel.objects.get(id=toursid)
            flag = True # 預設購物車中沒有相同的東西
            for unit in cartlist:
                # 有此商品，改變數量和總價
                # unit[0] 商品名稱 unit[1] 商品價格 unit[2] 商品數量 unit[3] 商品總價
                if tours.title == unit[0]: 
                    unit[2] = str(int(unit[2])+1) # 購物車中商品數量加1
                    unit[3] = str(int(unit[3])+tours.price) # 商品總價加上購物車中全部商品總價格
                    flag = False # 購物車中已有這項商品，所以為False
                    break
            # 沒有此商品，加入購物車
            if flag:
                templist = list()
                templist.append(tours.title) # 將商品一筆一筆的加入
                templist.append(str(tours.price))
                templist.append('1')
                templist.append(str(tours.price))
                cartlist.append(templist)
              
            # 更新session
            request.session['cartlist'] = cartlist
            return redirect('/cart/')
        
        else:
            return redirect('/tours/')
                        
    
    elif ctype == 'update':
        n = 0
        for unit in cartlist:
            amount = request.POST.get('qty'+str(n), '1') # 一筆一筆抓下來去更新。串列索引值由0開始，為方便認所以寫forloop.counter0
            if len(amount) == 0:
                amount = '1'
            if int(amount) <= 0: # 防止使用者寫負數
                amount = '1'
                
            unit[2] = amount
            unit[3] = str(int(unit[1])*int(unit[2]))
            n += 1
            
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
            
               
    elif ctype == 'delete':
        del cartlist[int(toursid)] # 將索引值刪除
        request.session['cartlist'] = cartlist # 將cartlist覆蓋
        return redirect('/cart/') # 並倒回購物車
    
    elif ctype == 'empty':
        cartlist.clear() # 將購物車清空
        request.session['cartlist'] = cartlist # 將cartlist覆蓋
        return redirect('/cart/') # 並導回購物車

#購物車到訂單(計算總價(加上運費))
def cartorder(request):
    if 'cusEmail' in request.session:
        global cartlist, guestname, guestphone, guestemail, guestaddress
        
        # 計算總價
        total = 0
        goodslist = cartlist
        for unit in cartlist:
            total += int(unit[3])
            
        if total >= 10000:
            shipping = 0
        else:
            shipping = 100
            
        grandtotal = total + shipping
        name = guestname
        phone = guestphone
        email = guestemail
        address = guestaddress
        
        return render(request, 'cartorder.html', locals())
    
    else:
        return redirect('/login')

#購物車確認
def cartok(request):
    if 'cusEmail' in request.session:
        if 'cuName' in request.POST:
            global cartlist, guestname, guestphone, guestemail, guestaddress, orderTotal, goodsTitle
            
            total = 0
            
            for unit in cartlist:
                total += int(unit[3])
                
            if total >= 10000:
                shipping = 0
            else:
                shipping = 100
                
            grandtotal = total + shipping
            orderTotal = grandtotal

            guestname = request.POST.get('cuName','') # 預設空白
            guestphone = request.POST.get('cuPhone', '')
            guestemail = request.POST.get('cuEmail', '')
            guestaddress = request.POST.get('cuAddress', '')
            payType = request.POST.get('paytype')
            
            # subtotal 小計
            unitorder = models.OrderModel.objects.create(subtotal=total, shipping=shipping, grandtotal=grandtotal, customename=guestname, customeemail=guestemail, customephone=guestphone, customeaddress=guestaddress, paytype=payType)
            
            # 寫明細
            for unit in cartlist:
                # unit[0] 商品名稱 unit[1] 商品價格 unit[2] 商品數量 unit[3] 商品總價
                goodsTitle.append(unit[0])
                # 小計
                total = int(unit[1])*int(unit[2])
                unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)

            # 訂單編號 (外來鍵：unitorder裡的流水編號)
            orderid = unitorder.id
            name = guestname
            email = guestemail
            
            cartlist.clear() # 清空結帳完購物車
            request.session['cartlist'] = cartlist # 清除session
            # 可加上推薦相關商品(您曾購買....為您推薦....)
            
            # 結帳頁面導轉
            if payType == '信用卡':
                return HttpResponseRedirect('/creditcard', locals())
            else:
                return render(request, 'cartok.html', locals())
        
        else:
            return redirect('/tours')
        
    # 如果沒有session (未登入)
    else:
        return redirect('/login')

#訂單明細
def cartordercheck(request):
    # orderid 從結帳頁面 cartok.html 送到這
    if 'orderid' in request.GET and 'guestemail' in request.GET and 'cusEmail' in request.session:
        orderid = request.GET.get('orderid', '')
        email = request.GET.get('guestemail', '')
        
        if orderid == '' or email == '':
            nosearch = 1 # 自訂值，代表找不到
        else:
            order = models.OrderModel.objects.filter(id=orderid, customeemail=email).first()
            if order == None: # 帳號錯誤
                notfound = 1
            else:
                details = models.DetailModel.objects.filter(dorder=order) # 用外來鍵 order 找出資料 
    
    return render(request, 'cartordercheck.html', locals())
            

#我的所有訂單
def myorder(request):
    if 'cusEmail' in request.session:
        email = request.session['cusEmail']
        order = models.OrderModel.objects.filter(customeemail=email)
        return render(request, 'myOrder.html', locals())
    
    else:
        return render(request, 'index.html')
    

#回報後五碼
def reportBank(request): 
    if 'orderid' in request.GET and 'guestemail' in request.GET:
        orderid = request.GET.get('orderid', '') # 預設空白
        guestemail = request.GET.get('guestemail', '')
        
        if orderid != '' and guestemail != '':
            bank = models.OrderModel.objects.filter(id=orderid, customeemail=guestemail, paytype='轉帳')
            if bank != None:
                return render(request, 'bankfive.html', locals())
            else:
                return render(request, 'product.html')
        
        else:
            return render(request, 'index.html')
        
    else:
        return render(request, 'index.html')
    
def bankfive(request):
    if 'orderid' in request.POST:
        orderid = request.POST['orderid']
        email = request.session['cusEmail']
        # 銀行後五碼
        bank = request.POST['bankfive']
        
        obj = models.OrderModel.objects.filter(id=orderid, customeemail=email, paytype='轉帳').count()
        if obj >0:
            data = models.OrderModel.objects.get(id=orderid) # 因為一定有值，所以用get
            data.bankaccount = bank
            data.save()
            
            order = models.OrderModel.objects.filter(customeemail=email)
            
            return render(request, 'myOrder.html', locals())
        
        else:
            return render(request, 'index.html')
    
    else:
        return render(request, 'index.html')
            
            
def ECPayCredit(request):
    
    global goodsTitle
    
    title = ""
    
    for unit in goodsTitle:
        title += unit + "#" # 綠界規則: 商品名稱需用#分隔
    
    
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,
        'TradeDesc': 'Travel.Django',
        'ItemName': title,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet/course',
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://member.lccnet.com.tw/',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }
    
    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html)
        return render(request, 'paycredit.html', locals())
        
        
    except Exception as error:
        print('An exception happened: ' + str(error))
        
        
        
        