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

def adminindex(request):
    
    return render_to_response('AdminIndex.html', locals(),context_instance=RequestContext(request))

def sblacklist(request):
    
    return render_to_response('sBlackList.html', locals(),context_instance=RequestContext(request))

def allshopowner(request):

	print request.GET.get('sellerName')
    return render_to_response('AllShopOwner.html', locals(),context_instance=RequestContext(request))

def approve(request):
    print request.GET.get('sellerName')
    return render_to_response('Approve.html', locals(),context_instance=RequestContext(request))

def cblacklist(request):
    
    return render_to_response('cBlackList.html', locals(),context_instance=RequestContext(request))

def allcustomer(request):
    
    return render_to_response('AllCustomer.html', locals(),context_instance=RequestContext(request))
