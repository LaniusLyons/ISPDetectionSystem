from mongoengine import *

class OrganizationProvider(Document):
	isp_name = StringField(max_length=50)
	organization_name = StringField(max_length=50)
	_id = IntField()


