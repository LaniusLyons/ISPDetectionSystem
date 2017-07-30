# -*- coding: utf-8 -*-\
from django.contrib.auth.models import User
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
import urllib
from django.http import JsonResponse
import django_smtp_ssl
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from django.template.loader import get_template

def send_email(email_to,subject,data):
	print 'enviando'
	from_email = 'IspFinderProject <'+settings.DEFAULT_FROM_EMAIL+'>'
	template = get_template('posting_email.html')
	context = Context(data)
	content = template.render(context)

	email = EmailMultiAlternatives(subject, None, from_email,email_to)
	email.attach_alternative(content, "text/html")
	try:
		email.send()
		print 'envio email'
		return True
	except Exception as e:
		print e

	return False


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
	list_client = None
	ip = get_client_ip(request)
	#delete next line for PROD Server
	ip = ['103.11.228.8','200.126.1.143','186.3.146.133','10.10.10.32','170.120.34.65','192.168.0.100']
	if isinstance(ip, list):
		isp = [x for x in ip if validateIP(x)]
		aux = getProvider(isp[0])

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
	response = None
	if request.user.is_authenticated():
		coords = request.session['coords'].split(',')
		lat = coords[1]
		lon = coords[0]
		ispIP = request.session['ispIP']
		ispName = request.session['ispName']
		ispUs = None
		if 'ispUs' in request.session:
			ispUs = request.session['ispUs']

		auth_token = authenticateAPI()
		if lat and lon and ispIP and ispName and auth_token:
			response = postAPICollaborator(lat,lon,ispIP,ispName,auth_token,request.user.email,ispUs)
		else:
			response = 400
	else:
		coords = request.GET.get('coords',None).split(',')
		lat = coords[1]
		lon = coords[0]
		ispIP = request.GET.get('ispIp',None)
		ispName = request.GET.get('ispName',None)
		ispUs = request.GET.get('ispUs',None)
		email = request.GET.get('email',None)

		auth_token = authenticateAPI()
		if lat and lon and ispIP and ispName and auth_token:
			response = postAPICollaborator(lat,lon,ispIP,ispName,auth_token,email,ispUs)
			admin = User.objects.all().filter(is_superuser=True).first()
			if admin:
				data = {'lat':lat,'lon':lon,'ispIP':ispIP,'ispName':ispName,'email':email,'ispUs':ispUs}
				send_email([admin.email],subject='Compartiendo informacion desde IspFinderProject',data=data)
		else:
			response = 400


	return redirect(reverse('logout' , args=(str(response),) ) )


def log_out(request, api_response):
	logout(request)
	return HttpResponseRedirect('/' + api_response)


def getIspPoints(Json):
	array = []
	for isp in Json:
		dict = {
			'latitud':isp[u'flat_location'][0],
			'longitud':isp[u'flat_location'][1],
			'isp':isp[u'isp_name']
		}
		array.append(dict)
	return array

def getColorMarker(Markers):
	dictionary = {}
	i = 0
	for marker in Markers:
		if marker[u'isp_name'] not in dictionary:
			dictionary[marker[u'isp_name']] = settings.COLORS[i]
			i = i + 1
	return dictionary

def getListClient(request):
	auth_token = authenticateAPI()
	if request.method == 'GET':
		if auth_token:
			headers = {'x-access-token': auth_token}
			r = requests.get(settings.URL_API + "/clientInfo/list",headers=headers)
			responseJson = json.loads(r.text)
			list = getIspPoints(responseJson)
			leyenda = getColorMarker(responseJson)
			return JsonResponse(dict(isp=list,leyenda=leyenda))
		else:
			return JsonResponse({'mensaje':'nada'})


def authenticateAPI():
	payload = {
		"user_name":"user_django",
		"password":"123456"
	}
	r = requests.post(settings.URL_API+'/authenticate' , data=payload )
	if r.status_code == 200:
		return r.json()['token']
	return None


def logOutAPI():
	r = requests.get(settings.URL_API + '/signOut')
	return r.status_code


def postAPICollaborator(lat,lon,ispIP,ispName,auth_token,email=None,ispUs=None):
	payload = {"email":email,
				"isp_ip":ispIP,
				"isp_name":ispName.lower().capitalize(),
				"isp_name_reported":ispUs,
				"latitude":lat,
				"longitude":lon}
	headers = {'x-access-token': auth_token}
	r = requests.post(settings.URL_API+'/clientInfo/insert', data=payload,headers=headers)
	return 200 if r.status_code == 200 or r.status_code == 201 else 400


def getProvider(providerIp):
	if providerIp:
		auth_token = authenticateAPI()
		if auth_token:
			headers = {'x-access-token': auth_token}
			payload = {'provider': providerIp}
			r = requests.get(settings.URL_API + '/providers/',params=payload,headers=headers)
			return r
	return None


def handlerError404(request):
	return render(request, '404.html',status=404)

def handlerError500(request):
	return render(request, '500.html',status=500)



