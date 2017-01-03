#coding=utf-8



from django.forms import ModelForm
from system.models import *
import time
import datetime
from PIL import Image
import hashlib

from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
import datetime
import random
import string
# Create your views here.

def adminlogin(request):
	adminMap={'admin':'admin'}
	if request.method=='POST':
		name=request.POST.get('adminName')
		passwd=request.POST.get('adminPassword')
		if adminMap.has_key(name):
			if adminMap[name]==passwd:
				request.session['UserName'] = name
				return HttpResponseRedirect('/adminindex/')
				#return render_to_response('Adminindex.html',locals(),context_instance=RequestContext(request))	
			else:
				return render_to_response('AdminLogin.html', locals(),context_instance=RequestContext(request))
		else:
			return render_to_response('AdminLogin.html', locals(),context_instance=RequestContext(request))
	else:
		return render_to_response('AdminLogin.html', locals(),context_instance=RequestContext(request))

def adminlogout(request):
	session = request.session.get('UserName', False)
	if session:
		del request.session['UserName']
	return HttpResponseRedirect('/adminlogin/')

def adminindex(request):
	if request.session.get('UserName', False):
		UserName = request.session['UserName']
		if UserName=='admin':
			return render_to_response('AdminIndex.html', locals(),context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/adminlogin/')
	else:
		return HttpResponseRedirect('/adminlogin/')
	
def authorzation(request):
	if request.method=='GET':
		arg=request.GET.get('Authorzation')
		arglist=arg.split('.')
		try:
			seller=Seller.objects.get(SellerAccount=arglist[0])
			seller.Authorzation=not (seller.Authorzation)
			print seller.Authorzation
			seller.save()
		except:
			print 'in except'
		Seller.objects.all()
	return HttpResponseRedirect('/allshopowner/')
	# return render_to_response('AllShopOwner.html',locals(),context_instance=RequestContext(request))

def sblacklist(request):
	sellerlist=[]
	sellerlistN=Seller.objects.all()
	for seller in sellerlistN:
		if len(BlacklistSeller.objects.filter(SellerID=seller))!=0:
			sellerlist.append(seller)
	return render_to_response('sBlackList.html', locals(),context_instance=RequestContext(request))

def delsblacklist(request):
	customerId=request.GET.get('sellerId')
	return render_to_response('sBlackList.html', locals(),context_instance=RequestContext(request))

def addsblacklist(request):
	sellerAccount=request.GET.get('sellerAccount')
	try:
		seller=Seller.objects.get(SellerAccount=sellerAccount)
		IsIn=BlacklistSeller.objects.filter(SellerID=seller)
		if len(IsIn)!=0:
			IsIn.delete()
		else:
			BlacklistSeller.objects.create(BlacklistSellerReason='no reason',SellerID=seller)
	except:
		print 'add blacklist'
	return render_to_response('sBlackList.html', locals(),context_instance=RequestContext(request))

def allshopowner(request):
	name=request.GET.get('sellerName')
	try:
		sellerlist=Seller.objects.all()
		# for seller in sellerlist:
		# 	if seller.Authorzation:
		# 		auz.append('true')
		# 	else:
	except:
		pass
	return render_to_response('AllShopOwner.html', locals(),context_instance=RequestContext(request))

def delseller(request):
	try:
		account=request.POST.get('sellerAccount')
		seller=Seller.objects.get(SellerAccount=account)
		shop=Shop.objects.filter(SellerID=seller).delete()
		Commodity.objects.filter(ShopID=shop).delete()
	except:
		print 'except'

	seller.delete()
	return HttpResponseRedirect('/allshopowner/')

def delcustomer(request):
	try:
		name=request.POST.get('customerName')
		customer=Customer.objects.get(CustomerName=name)
		Cart.objects.filter(CustomerID=customer).delete()
		Favorite.objects.filter(CustomerID=customer).delete()
	except:
		print 'except'
	customer.delete()
	return HttpResponseRedirect('/allcustomer/')

def approve(request):
#     print request.GET.get('sellerName')
    return render_to_response('Approve.html', locals(),context_instance=RequestContext(request))

def cblacklist(request):
	customerlist=[]
	customerlistN=Customer.objects.all()
	for customer in customerlistN:
		if len(BlacklistCustomer.objects.filter(CustomerID=customer))!=0:
			customerlist.append(customer)
	return render_to_response('cBlackList.html', locals(),context_instance=RequestContext(request))

def delcblacklist(request):
    customerId=request.GET.get('customerId')
    return render_to_response('cBlackList.html', locals(),context_instance=RequestContext(request))

def addcblacklist(request):
	customerAccount=request.GET.get('customerAccount')
	try:
		customer=Customer.objects.get(CustomerAccount=customerAccount)
		IsIn=BlacklistCustomer.objects.filter(CustomerID=customer)
		if len(IsIn)!=0:
			IsIn.delete()
		else:
			BlacklistCustomer.objects.create(BlacklistCustomerReason='no reason',CustomerID=customer)
	except:
		print 'add blacklist'
	return render_to_response('cBlackList.html', locals(),context_instance=RequestContext(request))

def allcustomer(request):
	if request.method=='GET':
		try:
			customerlist=Customer.objects.all()
			# for seller in sellerlist:
			# 	if seller.Authorzation:
			# 		auz.append('true')
			# 	else:
		except:
			pass
	return render_to_response('AllCustomer.html', locals(),context_instance=RequestContext(request))

def allshopownerquery(request):
	if request.method=='GET':
		account=request.GET.get('sellerAccount')
		try:
			sellerlist=Seller.objects.filter(SellerAccount__contains=account)
		except:
			pass
	return render_to_response('AllShopOwner.html', locals(),context_instance=RequestContext(request))

def allcustomerquery(request):
	if request.method=='GET':
		name=request.GET.get('customerName')
		try:
			customerlist=Customer.objects.filter(CustomerName__contains=name)
		except:
			pass
	return render_to_response('AllCustomer.html', locals(),context_instance=RequestContext(request))

def allorder(request):
	try:
		orderlist=OrderList.objects.all()
	except:
		print 'except'
		pass
	return render_to_response('AllOrder.html', locals(),context_instance=RequestContext(request))


def serachorder(request):
	if request.method=='GET':
		orderid=request.GET.get('orderId')
		try:
			orderlist=OrderList.objects.filter(id__contains=orderid)
		except:
			pass
	return render_to_response('AllOrder.html', locals(),context_instance=RequestContext(request))

def salehistory(request):
	salehistorylist=OrderList.objects.all()
	totalvalue=0
	scommission=2
	for salehistory in salehistorylist:
		totalvalue+=salehistory.SellPrice*salehistory.OrderAmount
	print totalvalue
	if request.method=='GET':
		commission=request.GET.get('commission')
		print totalvalue
		if not (commission is None):
			ctotalvalue=int(commission)*totalvalue/100
			scommission=commission
		else:
			ctotalvalue=int(scommission)*totalvalue/100
	return render_to_response('SaleHistory.html', locals(),context_instance=RequestContext(request))

def backupdatabase(request):

	return render_to_response('BackUpDataBase.html', locals(),context_instance=RequestContext(request))

def shopinfo(request):
	selleraccount=request.GET.get('selleraccount')
	try:
		seller=Seller.objects.get(SellerAccount=selleraccount)
		shoplist=Shop.objects.filter(SellerID=seller)
	except:
		pass
	return render_to_response('ShopInfo.html', locals(),context_instance=RequestContext(request))

def querycblacklist(request):
	customerAccount=request.GET.get('customerAccount')
	try:
		customerlist=Customer.objects.filter(CustomerAccount=customerAccount)
		for customer in customerlist:
			IsExist=BlacklistCustomer.objects.filter(CustomerID=customer)
			if len(IsExist)!=0:
				IsIn=1
			else:
				IsIn=0
	except:
		print 'add blacklist'
	return render_to_response('cBlackList.html',locals(),context_instance=RequestContext(request))

def querysblacklist(request):
	sellerAccount=request.GET.get('sellerAccount')
	print sellerAccount
	try:
		sellerlist=Seller.objects.filter(SellerAccount=sellerAccount)
		for seller in sellerlist:
			IsExist=BlacklistSeller.objects.filter(SellerID=seller)
			if len(IsExist)!=0:
				IsIn=1
			else:
				IsIn=0
			print IsIn
	except:
		print 'add blacklist'
	return render_to_response('sBlackList.html',locals(),context_instance=RequestContext(request))

def top5(request):
	shoplist=Shop.objects.all()
	return render_to_response('Top5.html', locals(),context_instance=RequestContext(request))

def addtotop5(request):
	toplist=request.POST.getlist('top5')
	TopShop.objects.all().delete()
	for top in toplist:
		try:
			shop=Shop.objects.get(id=top)
			TopShop.objects.create(ShopID=shop,SellerID=shop.SellerID,IsTop=1)
			top5list=TopShop.objects.all()
			shoplist=[]
			for top in top5list:
				try:
					shop=Shop.objects.get(id=top.ShopID.id)
					shoplist.append(shop)
				except:
					pass
		except:
			pass
	return render_to_response('Top5.html', locals(),context_instance=RequestContext(request))

def top10(request):

	return render_to_response('Top10.html', locals(),context_instance=RequestContext(request))

def commission(request):

	return render_to_response('Commission.html', locals(),context_instance=RequestContext(request))
