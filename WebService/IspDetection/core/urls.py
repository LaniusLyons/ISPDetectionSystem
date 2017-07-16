from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^[/]?(?P<api_response>\w{0,3}|)$',views.index, name='index'),
	url(r'^logs[/]$',views.logs, name='logs'),
	url(r'^login/$',views.login, name='login'),
	url(r'^logout/(?P<api_response>\w{0,3}|)[/]?$',views.log_out, name='logout'),
	url(r'^getIsp/$', views.getListClient, name='getListClient'),

	#url(r'^complete/facebook/$',views.index, name='index'),
	 
]
