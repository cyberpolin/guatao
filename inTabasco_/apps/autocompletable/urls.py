from django.conf.urls.defaults import patterns, url
from inTabasco_.apps.autocompletable.views import *

urlpatterns = patterns('',
	url(r'^ajaxautocompletable', ajaxautocompletable),
    url(r'^ajaxaubicacion', ajaxaubicacion),
    url(r'^ajaxacategoria', ajaxacategoria),
    url(r'^ajax_socio_vip', ajax_socio_vip),
	)