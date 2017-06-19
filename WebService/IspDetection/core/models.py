# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import hashlib
import random
import string
import time


def salt_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_hash():
	hash = hashlib.sha1()
	hash.update(str(time.time()).encode('utf-8')+salt_generator())
	hashfinal = hash.hexdigest()[:-10]
	return hashfinal

def generate_slug():
	return generate_hash()[:12]

# Create your models here.
class Provider(models.Model):
	id = models.AutoField(primary_key=True)
	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)
	name= models.CharField(max_length=140)
	nickname = models.CharField(max_length=140)

	class Meta:
		verbose_name = 'Provider'
		verbose_name_plural = 'Providers'
		db_table = 'Provider'

	def __unicode__(self):
		return self.name



class IP_Provider(models.Model):
	id = models.AutoField(primary_key=True)
	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)
	fk_provider = models.ForeignKey('Provider',related_name='providerIps',on_delete=models.CASCADE)
	city= models.CharField(max_length=140,blank=True,null=True)
	country = models.CharField(max_length=140,blank=True,null=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
	long = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)

	class Meta:
		verbose_name = 'IP_Provider'
		verbose_name_plural = 'IP_Providers'
		db_table = 'IP_Provider'

	def __unicode__(self):
		return self.fk_provider.name + ' gis: ' + self.lat + '/' + self.long



class Collaborator(User):
	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)

	class Meta:
		verbose_name = 'Collaborator'
		verbose_name_plural = 'Collaborators'
		db_table = 'Collaborator'

	def __unicode__(self):
		return self.username



class Geo_Collaborator(models.Model):
	id = models.AutoField(primary_key=True)
	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)
	fk_collaborator = models.ForeignKey('Collaborator',related_name='collaboratorGIS',on_delete=models.CASCADE)
	fk_provider_ws = models.ForeignKey('Provider',related_name='ispSetByWS',blank=True,null=True,on_delete=models.CASCADE)
	fk_provider_us = models.ForeignKey('Provider',related_name='ispSetByUser',blank=True,null=True,on_delete=models.CASCADE)
	verifiedIp = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
	long = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Geo_Collaborator'
		verbose_name_plural = 'Geo_Collaborators'
		db_table = 'Geo_Collaborator'

	def __unicode__(self):
		return self.fk_collaborator.slug + ' ISP: ' + self.fk_provider_ws
