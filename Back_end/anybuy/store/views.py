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

## Customer module
def helpcenter(request):
    return HttpResponse('Under Development!')

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
    commodity = Commodity.objects.get(id=cid)
    shop = commodity.ShopID
    commentlist = Comment.objects.filter(CommodityID = cid)
    try:
        isfavorite = Favorite.objects.get(CommodityID = cid, CustomerID = UserID)
    except Favorite.DoesNotExist:
        isfavorite = False
    return render_to_response('Customer_CommodityInfo.html', locals())

def getShop(request, cid):
    return HttpResponse('Under Development!')

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
    favoriteList = Favorite.objects.filter(CustomerID = UserID)
    return render_to_response('Customer_Favorite.html', locals())

def cart(request):
    return HttpResponse('Under Development!')

def add_to_cart(request, cid, amount, source):
    return HttpResponse('Under Development!')

def add_to_favorite(request):
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
    commodity = Commodity.objects.get(id = request.GET['id'])
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    Favorite.objects.create(FavoriteDate=date, CustomerID = user, CommodityID = commodity)
    return HttpResponse('You add: '+commodity.CommodityName)

def rm_from_cart(request):
    return HttpResponse('Under Development!')

def refreshcart(request):
    return HttpResponse('Under Development!')

def checkoutcart(request):
    return HttpResponse('Under Development!')

def bank(request):
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
    return render_to_response('bank.html',locals())

def bankaccount(request):
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
        user = Customer.objects.get(id=UserID)
    else:
        UserID = None
        UserType = None
        UserAccount = None
        user = None
    if 'id' in request.GET:
        commodity = Commodity.objects.get(id = request.GET['id'])
        Favorite.objects.get(CustomerID = user, CommodityID = commodity).delete()
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


## Shop Owner module
## By huangchaomin

def sellerentershop(request): #需要返回shoplist，shopadvlist，commodityadvlist
    if request.session.get('UserID', False):
        UserID = request.session['UserID']
        UserType = request.session['UserType']
        UserAccount = request.session['UserAccount']
    else:
        return HttpResponseRedirect('/login/')
    seller = Seller.objects.get(id=UserID)
    try:
        shop = Shop.objects.get(SellerID = seller)
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    # commodity = commoditylist[0]
    # shop = shopadvlist[0]
    # return HttpResponse(commoditylist[0].CommodityName)
    if shop and shop.Authorization:
        return render_to_response('Seller_EnterShop.html', locals())
    else:
        return HttpResponse('Under Authorization!')
def delfromshop(request, cid):
    Commodity.objects.get(id = cid).delete()
    return HttpResponse('You have deleted a commodity!!!')

#查看购买历史
def buysHistory(request, time):
    return HttpResponse('Under Development!')

def manageAD(request):
    return HttpResponse('Under Development!')

def changead(request):
    return HttpResponse('Under Development!')


def applyhomeshopadv(request):
    return HttpResponse('Under Development!')

def applyhomecommodityadv(request):
    return HttpResponse('Under Development!')

#定义表单模型
CommodityTypeChoices=(
    ('TH', 'TV & Home Theater'),
    ('CT', 'Computers & Tablets'),
    ('CP', 'Cell Phones'),
    ('CC', 'Cameras & Camcorders'),
    ('A', 'Audio'),
    ('CG', 'Car Electronics & GPS'),
    ('VM', 'Video,Games,Movies & Music'),
    ('HS', 'Health,Fitness & Sports'),
    ('HO', 'Home & Office'),
    ('O', 'Others')
)


class CommodityForm(forms.Form):
    CommodityName = forms.CharField(label='CommodityName', max_length=64)
    CommodityDescription = forms.CharField(label='Description')
    CommodityAmount = forms.IntegerField(label='Amount')
    SoldAmount = forms.IntegerField(label='Sold Amount')
    PurchasePrice = forms.FloatField(label='PurchasePrice')
    SellPrice = forms.FloatField(label='Sell Price')
    CommodityType = forms.ChoiceField(label='Type', choices=CommodityTypeChoices)
    CommodityImage = forms.ImageField(label='Image', required=False)  #,upload_to='images',max_length=255)
    CommodityDiscount = forms.FloatField(label='Discount')
    #ShopID = models.ForeignKey(Shop)
    IsAdv = forms.BooleanField(label='Is Adv?', required=False)

def add_and_modify(request, cid): # cid==0时添加新项目， !=0时修改cid的项目
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
        commoditylist = Commodity.objects.filter(ShopID = shop)
        shopadvlist = Shop.objects.filter(SellerID = seller, IsAdv = True)
        commodityadvlist = Commodity.objects.filter(ShopID = shop, IsAdv = True)
    except:
        shop = None
    if request.method == 'POST':
        cf = CommodityForm(request.POST, request.FILES)
        if cf.is_valid():
            #get form
            if int(cid) == 0:
                commodity = Commodity()
            else:
                commodity = Commodity.objects.get(id = cid)
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
            commodity = Commodity.objects.get(id = cid)
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
    seller = Seller.objects.get(id=UserID)
    if request.method == 'POST':
        sf = ShopForm(request.POST, request.FILES)
        if sf.is_valid():
            #get form
            shop = Shop()
            shop.ShopName = sf.cleaned_data['ShopName']
            shop.ShopDescription = sf.cleaned_data['ShopDescription']
            shop.BigImage = sf.cleaned_data['BigImage']
            shop.ShopImage = sf.cleaned_data['ShopImage']
            shop.SellerID = seller
            shop.IsAdv = True
            shop.IsHomeAdv = True
            shop.ShopState = 1
            shop.Authorization=False
            shop.save()
            return HttpResponseRedirect('/seller/home')
    else:
        sf = ShopForm()
    return render_to_response('addshop.html',locals(), context_instance=RequestContext(request))


#顾客管理订单（查看订单，申请退款，添加评论，修改评论。）
def manageOrder(request):
    return HttpResponse('Under Development!')


def apply_refund(request):
    return HttpResponse('Under Development!')

def cancel_refund(request):
    return HttpResponse('Under Development!')

def add_comment(request):
    return HttpResponse('Under Development!')

def confirm(request):
    return HttpResponse('Under Development!')

