# -*- coding: utf-8 -*-\
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from .models import *
from datetime import datetime
from social_django.models import UserSocialAuth
from netaddr import *


def validateIP(ip):
	if not IPAddress(ip).is_private() and not IPAddress(ip).is_netmask() and not IPAddress(ip).is_hostmask() and not IPAddress(ip).is_loopback() and not IPAddress(ip).is_reserved() and not IPAddress(ip).is_multicast():
		return True
	return False

def get_client_ip(request):
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	dir = settings.BASE_DIR + settings.LOGS_FOLDER + 'ip.logs.txt'
	if x_forwarded_for:
		remote = None
		if 'REMOTE_ADDR' in request.META:
			remote = request.META.get('REMOTE_ADDR') 	
		f = open(dir,'a')
		if remote:
			f.write(date+' // Forwarded-To: '+ x_forwarded_for +' // Remote: '+ remote +'\n')
		else:
			f.write(date+' // Forwarded-To: '+ x_forwarded_for +'\n')
		f.close()
		ip = x_forwarded_for.split(',')
	else:
		ip = request.META.get('REMOTE_ADDR')
		f = open(dir,'a')
		f.write(date+' // Remote-To:'+ip+'\n')
		f.close()
	return ip

# Create your views here.

def index(request):
	print 'index'
	print request.user
	ip = get_client_ip(request)
	ip = ['186.3.146.133', '10.10.10.32', '170.120.34.65','192.168.0.100']
	if isinstance(ip, list):
		print 'holi'
		isp = [x for x in ip if validateIP(x)]
		print isp
	return render(request,'index.html',{'isp_ip':isp[0]})


def logs(request):
	dir = settings.BASE_DIR + settings.LOGS_FOLDER + 'ip.logs.txt'
	f = open(dir,'r')
	content = f.readlines()
	f.close()
	return render(request,'logs.html',{'logs':content})


def login(request):
	print 'login'
	if request.user.is_authenticated():
		print 'yes'
	else:
		print 'no'
		print request.user
	return HttpResponseRedirect(reverse('index'))

def log_out(request):
	logout(request)
	return redirect('../')
