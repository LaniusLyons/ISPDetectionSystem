from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

# Register your models here.

#admin.site.unregister(User)
admin.site.register(Provider)
admin.site.register(IP_Provider)
admin.site.register(Collaborator)
admin.site.register(Geo_Collaborator)
