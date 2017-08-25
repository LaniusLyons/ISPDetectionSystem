# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.conf import settings
import hashlib
import random
import string
import time


def loadCredentials():
	import json
	import os
	with open(settings.BASE_DIR + settings.LOGS_FOLDER + 'credentials.json', 'rb') as data_file:
		data = json.loads(data_file.read())
		return data

credentialsPayload = loadCredentials()



def salt_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_hash():
	hash = hashlib.sha1()
	hash.update(str(time.time()).encode('utf-8')+salt_generator())
	hashfinal = hash.hexdigest()[:-10]
	return hashfinal

def generate_slug():
	return generate_hash()[:12]


def save_organization(sender, instance, **kwargs):
	from mongoengine import connect
	from .mongodb import OrganizationProvider
	connect('network_info_db')
	if kwargs['created']:
		entry = OrganizationProvider(isp_name=instance.fk_provider.name, organization_name=instance.name,_id=instance.pk).save()
	else:
		entry = OrganizationProvider.objects(_id=instance.pk).update(isp_name=instance.fk_provider.name, organization_name=instance.name)


def delete_organization(sender, instance, **kwargs):
	from mongoengine import connect
	from .mongodb import OrganizationProvider
	connect('network_info_db')
	OrganizationProvider.objects(_id=instance.pk).delete()


# Create your models here.

class Provider(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=140)

	class Meta:
		verbose_name = 'Proveedor'
		verbose_name_plural = 'Proveedores'
		db_table = 'Proveedor'

	def __unicode__(self):
		return self.name


class Organization(models.Model):
	id = models.AutoField(primary_key=True)
	fk_provider = models.ForeignKey('Provider',related_name='provider',on_delete=models.CASCADE)
	name = models.CharField(max_length=140)

	class Meta:
		verbose_name = 'Organizacion'
		verbose_name_plural = 'Organizaciones'
		db_table = 'Organizacion'

	def __unicode__(self):
		return self.name

post_save.connect(save_organization, sender=Organization)

post_delete.connect(delete_organization, sender=Organization)


# class IP_Provider(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)
# 	fk_provider = models.ForeignKey('Provider',related_name='providerIps',on_delete=models.CASCADE)
# 	city= models.CharField(max_length=140,blank=True,null=True)
# 	country = models.CharField(max_length=140,blank=True,null=True)
# 	lat = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
# 	long = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)

# 	class Meta:
# 		verbose_name = 'IP_Provider'
# 		verbose_name_plural = 'IP_Providers'
# 		db_table = 'IP_Provider'

# 	def __unicode__(self):
# 		return self.fk_provider.name + ' gis: ' + self.lat + '/' + self.long



class Collaborator(User):
	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)

	class Meta:
		verbose_name = 'Collaborator'
		verbose_name_plural = 'Collaborators'
		db_table = 'Collaborator'

	def __unicode__(self):
		return self.username



# class Geo_Collaborator(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	slug = models.SlugField(unique=True,blank=True,null=True,default=generate_slug)
# 	fk_collaborator = models.ForeignKey('Collaborator',related_name='collaboratorGIS',on_delete=models.CASCADE)
# 	fk_provider_ws = models.ForeignKey('Provider',related_name='ispSetByWS',blank=True,null=True,on_delete=models.CASCADE)
# 	fk_provider_us = models.ForeignKey('Provider',related_name='ispSetByUser',blank=True,null=True,on_delete=models.CASCADE)
# 	verifiedIp = models.BooleanField(default=False)
# 	lat = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
# 	long = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True)
# 	created_at = models.DateTimeField(auto_now_add=True)

# 	class Meta:
# 		verbose_name = 'Geo_Collaborator'
# 		verbose_name_plural = 'Geo_Collaborators'
# 		db_table = 'Geo_Collaborator'

# 	def __unicode__(self):
# 		return self.fk_collaborator.slug + ' ISP: ' + self.fk_provider_ws
