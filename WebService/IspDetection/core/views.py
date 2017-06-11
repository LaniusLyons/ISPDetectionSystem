# -*- coding: utf-8 -*-\
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from .models import *
from datetime import datetime


def get_client_ip(request):
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	dir = settings.BASE_DIR + '/django_project/ip.logs.txt'
	if x_forwarded_for:
		f = open(dir,'a')
		f.write(date+'forwarded-To:'+x_forwarded_for+'\n')
		f.close()
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
		f = open(dir,'a')
		f.write(date+'remote-To:'+ip+'\n')
		f.close()
	return ip

# Create your views here.

def index(request):
	ip = get_client_ip(request)
	return render(request,'index.html',{'IP':ip})
