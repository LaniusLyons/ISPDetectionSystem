from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Provider)
admin.site.register(IP_Provider)
admin.site.register(Collaborator)
admin.site.register(Geo_Collaborator)
