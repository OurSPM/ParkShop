#coding=utf-8

from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from system.models import *
import time
import datetime
from PIL import Image
import hashlib
# Create your views here.

def addr(request):
    if request.session.get('UserID', False):
            UserID = request.session['UserID']
            UserType = request.session['UserType']
            UserAccount = request.session['UserAccount']
            UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        checkcustomer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    try:
        currentCustomer=Customer.objects.get(CustomerAccount=UserName)
    except:
        return HttpResponseRedirect('/index')
    if request.method=='POST':
        print 'in post'
        content=request.POST.get('cont').split('.')
        if len(content)==2:
            address=content[0]
            telephone=content[1]
            exist=CommodityReceiveAddress.objects.filter(CustomerID=UserID,CommodityAddress=address,CommodityTelephone=telephone)
            AddressID=-1
            if len(exist)==0:
                AddressID=CommodityReceiveAddress.objects.create(CustomerID=currentCustomer,CommodityAddress=address,CommodityTelephone=telephone).id
            else:
                for onlyID in exist:
                    AddressID=onlyID.id
        print "AddressID:%s" %AddressID
        return render_to_response('bankaccount.html', locals())
    else:
        print 'not in post'
        AddrList=CommodityReceiveAddress.objects.filter(CustomerID=UserID)
        rootAddr=currentCustomer
        return render_to_response('Customer_addr.html', locals(),context_instance=RequestContext(request))

def helpcenter(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    return render_to_response('helpcenter.html', locals())

def getCommodity(request, cid):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        commodity = Commodity.objects.get(id=cid)
        shop = commodity.ShopID
        commentlist = Comment.objects.filter(CommodityID = cid)
    except:
        return HttpResponseRedirect('/index')
    try:
        isfavorite = Favorite.objects.get(CommodityID = cid, CustomerID = UserID)
    except Favorite.DoesNotExist:
        isfavorite = False
    return render_to_response('Customer_CommodityInfo.html', locals())

def getShop(request, cid):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        shop = Shop.objects.get(id=cid)
        commodityList = Commodity.objects.filter(ShopID = shop,IsAdv=True)
        shopList = Shop.objects.filter(SellerID = shop.SellerID)
    except:
        return HttpResponseRedirect('/index')
    return render_to_response('Customer_EnterShop.html', locals())

def favorite(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    favoriteList = Favorite.objects.filter(CustomerID = UserID)
    return render_to_response('Customer_Favorite.html', locals())

def cart(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login')
    cartList = Cart.objects.filter(CustomerID = UserID)
    total=0
    carEmpty=0
    if len(cartList)==0:
        carEmpty=1
    for cart in cartList:
        total = total+cart.CartCommodityAmount*cart.CommodityID.SellPrice
    return render_to_response('Customer_MyCart.html', locals())

def add_to_cart(request, cid, amount, source):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        user = Customer.objects.get(id=UserID)
        try:
            commodity = Commodity.objects.get(id = cid)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    try:
        cart = Cart.objects.get(CustomerID = user, CommodityID = commodity)
        cart.CartCommodityAmount = cart.CartCommodityAmount+1
        cart.save()
    except Cart.DoesNotExist:
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        Cart.objects.create(CartDate=date, CustomerID = user, CommodityID = commodity, CartCommodityAmount = int(amount))
    if source == 'commodity':
        return HttpResponseRedirect('/commodity/id/'+cid)
    else:
        return HttpResponseRedirect('/favorite/')
    #return render_to_response('Customer_CommodityInfo.html', locals())

def add_to_favorite(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        try:
            user = Customer.objects.get(id=UserID)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    try:
        commodity = Commodity.objects.get(id = request.GET['id'])
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        Favorite.objects.create(FavoriteDate=date, CustomerID = user, CommodityID = commodity)
    except:
        return HttpResponseRedirect('/index')
    return HttpResponse('You add: '+commodity.CommodityName)

def rm_from_cart(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        try:
            user = Customer.objects.get(id=UserID)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    if 'id' in request.GET:
        try:
            commodity = Commodity.objects.get(id = request.GET['id'])
            Cart.objects.get(CustomerID = user, CommodityID = commodity).delete()
        except:
            return HttpResponseRedirect('/index')
    else:
        commodity = None
    return HttpResponse('You removed: '+commodity.CommodityName)

def refreshcart(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        try:
            user = Customer.objects.get(id=UserID)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    if 'id' in request.GET:
        try:
            commodity = Commodity.objects.get(id = request.GET['id'])
            cart = Cart.objects.get(CustomerID = user, CommodityID = commodity)
            cart.CartCommodityAmount = int(request.GET['amount'])
            cart.save()
        except:
            return HttpResponseRedirect('/index')
    else:
        commodity = None
    return HttpResponse('You refresh: '+commodity.CommodityName)

def checkoutcart(request,cid):
    print 'in to checkoutcart'
    print 'AddressID:%s' %cid
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        try:
            user = Customer.objects.get(id=UserID)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    try:
        AddressID=CommodityReceiveAddress.objects.get(id=cid)
        cutomerorder = CustomerOrder.objects.create(CommodityAddressID=AddressID,CustomerOrderState=0, CustomerOrderDate=date, CustomerID=user)
    except:
        return HttpResponseRedirect('/index')
        # 从购物车中删除，现在是将checkbox注释了，所以这里是删除购物车中所有物品
    commoditylist = Cart.objects.filter(CustomerID=user)
    index=0
    shoporderlist=[]
    for commodity in commoditylist:
        shoporder= ShopOrder.objects.create(CommodityAddressID=AddressID,ShopOrderState=0, ShopOrderDate=date, ShopID=commoditylist[index].CommodityID.ShopID)
        shoporderlist.append(shoporder) 
        index+=1
    
    index=0
    for commodity in commoditylist:
        print 'in for commoditylist'
        orderlist = OrderList.objects.create(CommodityAddressID=AddressID,OrderListState=0, OrderListDate=date, OrderAmount = commodity.CartCommodityAmount, CustomerOrderID=cutomerorder, ShopOrderID=shoporderlist[index],CommodityName=commodity.CommodityID.CommodityName,SellPrice=commodity.CommodityID.SellPrice,CommodityImage=commodity.CommodityID.CommodityImage )
        index+=1
        print commodity.CommodityID
        try:
            print 'in try'
            perCommodity=Commodity.objects.get(id=commodity.CommodityID.id)
            perCommodity.CommodityAmount-=commodity.CartCommodityAmount
            print 'commodity.CartCommodityAmount:%d' %(commodity.CartCommodityAmount)
            print 'perCommodity.CommodityAmount:%d' %(perCommodity.CommodityAmount)
            perCommodity.save()
        except:
            pass
        # 从购物车中删除，现在是将checkbox注释了，所以这里是删除购物车中所有物品
    Cart.objects.filter(CustomerID = user).delete()
    return HttpResponseRedirect('/')

def bank(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    try:
        user = Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    return render_to_response('bank.html',locals())

def bankaccount(request):
    print "in to bankaccount"
    if request.session.get('UserID', False):

        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        user = Customer.objects.get(id=UserID)
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    return render_to_response('bankaccount.html', locals())

def rm_from_favorite(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
        try:
            user = Customer.objects.get(id=UserID)
        except:
            return HttpResponseRedirect('/index')
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    if 'id' in request.GET:
        try:
            commodity = Commodity.objects.get(id = request.GET['id'])
            Favorite.objects.get(CustomerID = user, CommodityID = commodity).delete()
        except:
            return HttpResponseRedirect('/index')
    else:
        commodity = None
    return HttpResponse('You removed: '+commodity.CommodityName+'from favorite')

def search(request, keyword):  #/search/keyword/ 以keyword为关键字进行搜索，返回一个commodityList
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
    else:
        UserID = None
        UserType = None
        UserAccount = None
    commodityList = Commodity.objects.filter(CommodityName__contains = keyword)
    commodityList_by_amount = commodityList.order_by('SoldAmount')
    commodityList_by_price = commodityList.order_by('SellPrice')
    commodityList_by_counterprice = commodityList.order_by('-SellPrice')
    return render_to_response('Customer_CommodityList.html', locals())

def searchInShop(request, lkeyword):
    print "get little search!"
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
    else:
        UserID = None
        UserType = None
        UserAccount = None
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    try:
        shop = Shop.objects.get(SellerID = seller)
        commoditylist = Commodity.objects.filter(ShopID = shop,CommodityName__contains=lkeyword)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    return render_to_response('Seller_EnterShop.html', locals())

def CustomerSearchInShop(request, lkeyword,cid):
    print "customer in little search!"
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
    else:
        UserID = None
        UserType = None
        UserAccount = None
        return HttpResponseRedirect('/login/')
    try:
        shop=Shop.objects.get( id= cid)
        commodityList = Commodity.objects.filter(ShopID = cid,CommodityName__contains=lkeyword)
    except:
        pass
    return render_to_response('Customer_EnterShop.html', locals())

def sellerentershop(request): #需要返回shoplist，shopadvlist，commodityadvlist
    print 'go into enter shop'
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        print UserID
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    
    try:
        shop = Shop.objects.get(SellerID = seller)
    except:
        shop=None
     
    if shop is None:
        return HttpResponseRedirect('/addshop')
    elif seller.Authorzation==False:
        return render_to_response('authorzation.html',locals())
    else:
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
        return render_to_response('Seller_EnterShop.html', locals())

def delfromshop(request, cid):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        Commodity.objects.get(id = cid).delete()
    except:
        return HttpResponseRedirect('/index')
    return HttpResponse('You have deleted a commodity!!!')

#查看购买历史
def buysHistory(request, time):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    # shopID = Customer.objects.get(Customer = UserID)
    shopOrder = CustomerOrder.objects.filter(CustomerID = UserID)
    BuysHistoryList = []
    now = datetime.datetime.now()
    for so in shopOrder:
        BuyList = OrderList.objects.filter(CustomerOrderID = so)
        for sl in BuyList:
            if time == "all":
                BuysHistoryList.append(sl)
            elif time == "year":
                if sl.OrderListDate.year == now.year:
                    BuysHistoryList.append(sl)
            elif time == "month":
                if sl.OrderListDate.month == now.month and sl.OrderListDate.year == now.year:
                    BuysHistoryList.append(sl)
            elif time == "day":
                if sl.OrderListDate.day == now.day and sl.OrderListDate.month == now.month and sl.OrderListDate.year == now.year:
                    BuysHistoryList.append(sl)
    totalvalue = 0
    for shl in BuysHistoryList:
        totalvalue = totalvalue + shl.SellPrice * shl.OrderAmount
    return render_to_response('Customer_BuyHistory.html', locals())

def manageAD(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    try:
        shop = Shop.objects.get(SellerID = seller)
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    # commodity = commoditylist[0]
    shoplist = Shop.objects.filter(SellerID = seller)
    # shop = shopadvlist[0]
    commoditylist = Commodity.objects.filter(ShopID = shop)
    # return HttpResponse(shopadvlist[0])
    return render_to_response('manageAD.html', locals())

def changead(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/index')
    try:
        shop = Shop.objects.get(SellerID = seller)
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    cid = request.GET['id']
    try:
        commodity = Commodity.objects.get(id=cid)
        isadv = commodity.IsAdv
    except:
        return HttpResponseRedirect('/index')
    if isadv:
        commodity.IsAdv = False
    else:
        commodity.IsAdv = True
    commodity.save()
    return HttpResponse("You change the ad state")

def applyhomeshopadv(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/index')
    try:
        shop = Shop.objects.get(SellerID = seller)
    except:
        shop = None
    ishomeadv = shop.IsHomeAdv
    if ishomeadv:
        shop.IsHomeAdv = False
        HomeShopAdv.objects.get(ShopID=shop).delete()
    else:
        shop.IsHomeAdv = True
        admin=Administrator.objects.get(id=1)
        HomeShopAdv.objects.create(ShopID=shop, OwnerID=admin, AdvertisementContent=shop.ShopName, ApplyState=False)
    shop.save()
    return HttpResponse("You apply the home shop ad state")

def applyhomecommodityadv(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    seller = Seller.objects.get(id=UserID)
    try:
        shop = Shop.objects.get(SellerID = seller)
    except:
        shop = None
    cid = request.GET['id']
    commodity = Commodity.objects.get(id=cid)
    ishomeadv = commodity.IsHomeAdv
    if ishomeadv:
        commodity.IsHomeAdv = False
        HomeCommodityAdv.objects.get(CommodityID=commodity).delete()
    else:
        commodity.IsHomeAdv = True
        admin=Administrator.objects.get(id=1)
        HomeCommodityAdv.objects.create(CommodityID=commodity, OwnerID=admin, AdvertisementContent=commodity.CommodityName, ApplyState=False)
    commodity.save()
    return HttpResponse("You change the ad state")

#定义表单模型
CommodityTypeChoices=(
        ('C','TV& Home Theater'),
        ('A','Computers & Tablets'),
        ('S','Cell Phones'),
        ('J','Cameras & Camcorders'),
        ('D','Audio'),
        ('H','Car Electronics & GPS'),
        ('M','Video, Games, Movies & Music'),
        ('F','Health, Fitness & Sports'),
        ('E','Home & Office'),
        ('O','Others')
)


class CommodityForm(forms.Form):
    CommodityName = forms.CharField(label='CommodityName', max_length=64)
    CommodityDescription = forms.CharField(label='Description')
    CommodityAmount = forms.IntegerField(label='Amount')
    SoldAmount = forms.IntegerField(label='SoldAmount')
    PurchasePrice = forms.FloatField(label='PurchasePrice')
    SellPrice = forms.FloatField(label='SellPrice')
    CommodityType = forms.ChoiceField(label='Type', choices=CommodityTypeChoices)
    CommodityImage = forms.ImageField(label='Image', required=False)  #,upload_to='images',max_length=255)
    CommodityDiscount = forms.FloatField(label='Discount')
    ShopID = models.ForeignKey(Shop)
    IsAdv = forms.BooleanField(label='Is Adv?', required=False)

def add_and_modify(request, cid): # cid==0时添加新项目， !=0时修改cid的项目
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    try:
        shop = Shop.objects.get(SellerID = seller)
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    if request.method == 'POST':
        cf = CommodityForm(request.POST, request.FILES)
        if cf.is_valid():
            if int(cid) == 0:
                commodity = Commodity()
            else:
                try:
                    commodity = Commodity.objects.get(id = cid)
                except:
                    return HttpResponseRedirect('/index')
            commodity.CommodityName = cf.cleaned_data['CommodityName']
            commodity.CommodityDescription = cf.cleaned_data['CommodityDescription']
            commodity.CommodityAmount = cf.cleaned_data['CommodityAmount']
            commodity.SoldAmount = cf.cleaned_data['SoldAmount']
            commodity.PurchasePrice = cf.cleaned_data['PurchasePrice']
            commodity.SellPrice = cf.cleaned_data['SellPrice']
            commodity.CommodityType = cf.cleaned_data['CommodityType']
            commodity.CommodityImage = cf.cleaned_data['CommodityImage']
            commodity.CommodityDiscount = cf.cleaned_data['CommodityDiscount']
            commodity.IsAdv = cf.cleaned_data['IsAdv']
            commodity.IsHomeAdv = True
            commodity.ShopID = shop
            # image = request.FILES["CommodityImage"]
            commodity.save() 
            return HttpResponseRedirect('/seller/home')
    else:
        cf = CommodityForm()
        if int(cid) != 0: # 如果cid!=0 就代表要修改的CommodityID
            try:
                commodity = Commodity.objects.get(id = cid)
            except:
                return HttpResponseRedirect('/index')
            data={
            'CommodityName' : commodity.CommodityName,
            'CommodityDescription' : commodity.CommodityDescription,
            'CommodityAmount' : commodity.CommodityAmount,
            'SoldAmount' : commodity.SoldAmount,
            'PurchasePrice' : commodity.PurchasePrice,
            'SellPrice' : commodity.SellPrice,
            'CommodityType' : commodity.CommodityType,
            'CommodityImage' : commodity.CommodityImage,
            'CommodityDiscount' : commodity.CommodityDiscount,
            'IsAdv' : commodity.IsAdv,
            }
            cf = CommodityForm(data)
    return render_to_response('manageCommodity.html',locals(), context_instance=RequestContext(request))

class ShopForm(forms.Form):
    ShopName = forms.CharField(label='ShopName')
    ShopDescription = forms.CharField(label='Description', required=False)
    #店铺状态：0-待审核，1-营业，2-歇业
    BigImage = forms.ImageField(label='BigImage', required=False)
    ShopImage = forms.ImageField(label='ShopImage', required=False)

def add_and_modify_shop(request): # cid==0时添加新项目， !=0时修改cid的项目
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        return HttpResponseRedirect('/login/')
    try:
        seller = Seller.objects.get(id=UserID) 
    except:
        print 'add shop except'
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        sf = ShopForm(request.POST, request.FILES)
        if sf.is_valid():
            #get form
            shopexist=Shop.objects.filter(SellerID=seller)
            if shopexist:
                print 'get shop evial post'
                return render_to_response('shopexist.html')
            else:
                print 'add shop continue'
            shop = Shop()
            shop.ShopName = sf.cleaned_data['ShopName']
            shop.ShopDescription = sf.cleaned_data['ShopDescription']
            shop.BigImage = sf.cleaned_data['BigImage']
            shop.ShopImage = sf.cleaned_data['ShopImage']
            shop.SellerID = seller
            shop.IsAdv = True
            shop.IsHomeAdv = True
            shop.ShopState = 1
            shop.save()
            if seller.SellerEmailCodeFlag:
                return HttpResponseRedirect('/')
            else:
                return render_to_response('cuole.html')
    else:
        sf = ShopForm()
    return render_to_response('addshop.html',locals(), context_instance=RequestContext(request))


#顾客管理订单（查看订单，申请退款，添加评论，修改评论。）
def manageOrder(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    try:
        customer=Customer.objects.get(id=UserID)
    except:
        return HttpResponseRedirect('/login/')
    customerOrder = CustomerOrder.objects.filter(CustomerID = UserID)
    orderList = []
    for so in customerOrder:
        List = OrderList.objects.filter(CustomerOrderID = so)
        for ol in List:
            orderList.append(ol)
    #return HttpResponse(orderList[0])
    return render_to_response('manageOrder.html', locals())

def apply_refund(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    if 'id' in request.GET:
        ol = OrderList.objects.get(id = request.GET['id'])
        ol.OrderListState = 4
        ol.save()
        so = ShopOrder.objects.get(id = ol.ShopOrderID.id)
        so.ShopOrderState = 4
        so.save()
        co = CustomerOrder.objects.get(id = ol.CustomerOrderID.id)
        co.CustomerOrderState = 4
        co.save()
    else:
        ol = None
    return HttpResponse("You modified: "+ ol.CommodityName+"from Orderlist")

def cancel_refund(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    if 'id' in request.GET:
        ol = OrderList.objects.get(id = request.GET['id'])
        ol.OrderListState = 7
        ol.save()
        so = ShopOrder.objects.get(id = ol.ShopOrderID.id)
        so.ShopOrderState = 7
        so.save()
        co = CustomerOrder.objects.get(id = ol.CustomerOrderID.id)
        co.CustomerOrderState = 7
        co.save()
    else:
        ol = None
    return HttpResponse("You modified: "+ ol.CommodityName+"from Orderlist")

def add_comment(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    if 'id' in request.GET:
        try:
            ol = OrderList.objects.get(id = request.GET['id'])
            ol.OrderListState = 8
            ol.save()
            so = ShopOrder.objects.get(id = ol.ShopOrderID.id)
            so.ShopOrderState = 8
            so.save()
            co = CustomerOrder.objects.get(id = ol.CustomerOrderID.id)
            co.CustomerOrderState = 8
            co.save()
            content = request.GET['content']
        except:
            return HttpResponseRedirect('/index')
        try:
            commodity=Commodity.objects.get(CommodityImage=ol.CommodityImage)
        except:
            print 'comment '
            commodity=None
        Comment.objects.create(CommentContent = content, CustomerID = ol.CustomerOrderID.CustomerID, CommodityID = commodity)
    else:
        ol = None
    return HttpResponse("You comment: "+ ol.CommodityName+"from Orderlist")

def confirm(request):
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
        UserName = UserAccount
    else:
        UserID = None
        UserType = None
        UserAccount = None
    if 'id' in request.GET:
        try:
            ol = OrderList.objects.get(id = request.GET['id'])
            ol.OrderListState = 7 # change to 7 for easy operation
            ol.save()
            so = ShopOrder.objects.get(id = ol.ShopOrderID.id)
            so.ShopOrderState = 7
            so.save()
            co = CustomerOrder.objects.get(id = ol.CustomerOrderID.id)
            co.CustomerOrderState = 7
            co.save()
            content = request.GET['content']
        except:
            return HttpResponseRedirect('/index')
        try:
            commodity=Commodity.objects.get(CommodityImage=ol.CommodityImage)
        except:
            print 'confirm '
            commodity=None
        Comment.objects.create(CommentContent = content, CustomerID = ol.CustomerOrderID.CustomerID, CommodityID = commodity)
    else:
        ol = None
    return HttpResponse("You comment: "+ ol.CommodityName+"from Orderlist")

