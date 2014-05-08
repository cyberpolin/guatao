from django.conf.urls import patterns, url
from inTabasco_.apps.movil.views import *

urlpatterns = patterns('',
    #url(r'^editar_socio/(?P<id_socio>\d+)', editar_socio),
    url(r'^movil/espacios/(?P<pk>\d+)', lista_espacios, name="lista_espacios"),
    url(r'^movil/nuevo-socio-pk/(?P<pk>\d+)', nuevo_socio_pk, name='nuevo_socio_pk'),
    url(r'^movil/nuevo-socio/', nuevo_socio, name='nuevo_socio'),
    url(r'^movil/resetear-password/(?P<pk>\d+)', reset_pasword, name='reset_pasword'),
	url(r'^movil/login/', loginView, name='loginView'),
    url(r'^movil/$', index, name='index'),
    )