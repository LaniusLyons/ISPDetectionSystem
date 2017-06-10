# -*- coding: utf-8 -*-\
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from .models import *


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	dir = settings.BASE_DIR + '/IspDetection/ip.logs.txt'
	if x_forwarded_for:
		f = open(dir,'r+')
		f.write('To:'+x_forwarded_for+'\n')
		f.close()
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

# Create your views here.

def index(request):
	ip = get_client_ip(request)
	return render(request,'index.html',{'IP':ip})
