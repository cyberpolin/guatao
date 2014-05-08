from django.conf.urls import patterns, url
from inTabasco_.apps.correos.views import *

urlpatterns = patterns('',
	url(r'^reset_password/', reset_password),	
	)