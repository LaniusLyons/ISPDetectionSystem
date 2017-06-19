# -*- coding: utf-8 -*-\
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from .models import *
from datetime import datetime
from social_django.models import UserSocialAuth


def get_client_ip(request):
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	dir = settings.BASE_DIR + settings.LOGS_FOLDER + 'ip.logs.txt'
	if x_forwarded_for:
		remote = None
		if 'REMOTE_ADDR' in request.META:
			remote = request.META.get('REMOTE_ADDR') 	
		f = open(dir,'a')
		f.write(date+' // Rorwarded-To: '+ x_forwarded_for +' // Remote: '+ remote +'\n')
		f.close()
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
		f = open(dir,'a')
		f.write(date+' // Remote-To:'+ip+'\n')
		f.close()
	return ip

# Create your views here.

def index(request):
	ip = get_client_ip(request)
	return render(request,'index.html',{'IP':ip})


def logs(request):
	dir = settings.BASE_DIR + settings.LOGS_FOLDER + 'ip.logs.txt'
	f = open(dir,'r')
	content = f.readlines()
	f.close()
	return render(request,'logs.html',{'logs':content})


def log_out(request):
	logout(request)
