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
		name=request.POST.get('sellerName')
		seller=Seller.objects.get(SellerName=name)
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
		name=request.GET.get('sellerName')
		try:
			sellerlist=Seller.objects.filter(SellerName__contains=name)
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

	return render_to_response('SerachOrder.html', locals(),context_instance=RequestContext(request))
