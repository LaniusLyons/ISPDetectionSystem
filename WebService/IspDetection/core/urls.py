from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^logs[/]$',views.logs, name='logs'),
	url(r'^login/$',views.login, name='login'),
	url(r'^logout/$',views.log_out, name='logout'),

	#url(r'^complete/facebook/$',views.index, name='index'),
	 
]
