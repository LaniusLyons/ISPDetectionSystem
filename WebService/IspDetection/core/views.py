# -*- coding: utf-8 -*-\
from _mysql import result

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from .models import *
from datetime import datetime
from netaddr import *
import requests
import pprint
import json


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


def index(request,api_response=None):
	print 'index'
	ip = get_client_ip(request)
	#delete next line for PROD Server
	ip = ['186.3.146.133', '10.10.10.32', '170.120.34.65','192.168.0.100']
	if isinstance(ip, list):
		isp = [x for x in ip if validateIP(x)]
		aux = getProvider(isp[0])
		print aux.json()
	logOutAPI()
	return render(request,'index.html',{'ispInfo':aux.json(),'ispIp':isp[0], 'response':switch(api_response)})


def switch(argument):
	switcher = {
		'200':"GOOD_STATUS",
		'400':"BAD_STATUS",
	}
	return switcher.get(argument,"Nada")


def logs(request):
	dir = settings.BASE_DIR + settings.LOGS_FOLDER + 'ip.logs.txt'
	f = open(dir,'r')
	content = f.readlines()
	f.close()
	return render(request,'logs.html',{'logs':content})


def login(request):
	print 'login'
	print request.session['coords']
	response = None
	if request.user.is_authenticated():
		coords = request.session['coords'].split(',')
		lat = coords[0]
		lon = coords[1]
		ispIP = request.session['ispIP']
		ispName = request.session['ispName']
		ispUs = None
		if 'ispUs' in request.session:
			ispUs = request.session['ispUs']
		print lat, lon, ispName, ispIP
		is_authenticated = authenticateAPI()
		if lat and lon and ispIP and ispName and is_authenticated == 200:
			response = postAPICollaborator(request.user,lat,lon,ispIP,ispName,ispUs)
		else:
			response = 400

	return redirect(reverse('logout' , args=(str(response),) ) )


def log_out(request, api_response):
	print 'logout'
	logout(request)
	return HttpResponseRedirect('/' + api_response)


def authenticateAPI():
	payload = {
		"user_name":"user_django",
		"password":"123456"
	}
	r = settings.SESSION.post(settings.URL_API+'/authenticate' , data=payload )
	return r.status_code


def getListClient(request):
	is_authenticated = authenticateAPI()
	if is_authenticated:
		r = settings.SESSION.get(settings.URL_API + '/clientInfo/list')
		return JsonResponse(r.json(),safe=False)
	return JsonResponse({})


def logOutAPI():
	r = settings.SESSION.get(settings.URL_API + '/signOut')
	return r.status_code


def postAPICollaborator(user,lat,lon,ispIP,ispName,ispUs=None):
	payload = {"email":user.email,
			   "isp_ip":ispIP,
			   "isp_name":ispName,
			   "isp_name_reported":ispUs,
			   "latitude":lat,
			   "longitude":lon}
	r = settings.SESSION.post(settings.URL_API+'/clientInfo/insert', data=payload)
	return 200 if r.status_code == 200 or r.status_code == 201 else 400


def getProvider(providerIp):
	if providerIp:
		is_authenticated = authenticateAPI()
		if is_authenticated:
			r = settings.SESSION.get(settings.URL_API + '/providers/'+providerIp)
			return r
	return None