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

# Create your views here.


def index(request,api_response=None):
	print 'index'
	ip = get_client_ip(request)
	ip = ['186.3.146.133', '10.10.10.32', '170.120.34.65','192.168.0.100']
	if isinstance(ip, list):
		isp = [x for x in ip if validateIP(x)]
		aux = requests.get('http://ip-api.com/json/'+isp[0])
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
	responseGet = None
	if request.user.is_authenticated():
		coords = request.session['coords'].split(',')
		lat = coords[0]
		lon = coords[1]
		response = postAPICollaborator(request.user,lat,lon)

	return redirect(reverse('logout' , args=(str(responseGet),) ) )

def log_out(request, api_response):
	logout(request)
	return HttpResponseRedirect('/' + api_response)

def loginAPI():
	payload = {
		"user_name":"user_django",
		"password":"123456"
	}
	r = settings.SESSION.post(settings.URL_API+"/authenticate" , data=payload )
	pprint.pprint(r.text)
	return r.status_code

def getClient():
	r = settings.SESSION.get(settings.URL_API + "/clientInfo/list")
	pprint.pprint(r.text)
	return r.status_code

def postAPICollaborator(user,lat,lon):
	payload = {"email":"metacris93@hotmail.com",
			   "username":user.username,
			   "fk_provider":"186.3.146.108",
			   "lat":lat,
			   "lon":lon}
	headers = {"content-type": "application/json", "accept": "application/json"}
	r = requests.post( settings.URL_API+'/collaborators', data=json.dumps(payload), headers=headers ) # url , data , json, kwargs
	return 200 if r.status_code == 200 else 400


