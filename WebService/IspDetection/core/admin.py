from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name','fk_provider',)

#admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Organization,OrganizationAdmin)
admin.site.register(Provider)
#admin.site.register(IP_Provider)
#admin.site.register(Collaborator)
#admin.site.register(Geo_Collaborator)
