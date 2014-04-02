from django.conf.urls import patterns, url
from inTabasco_.apps.Login.views import *

urlpatterns = patterns('',
	url(r'^validar/', validar),	
	url(r'^logout_user/', logout_user),
    url(r'^login_/', login_)
	)