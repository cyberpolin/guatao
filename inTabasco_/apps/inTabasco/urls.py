from django.conf.urls import patterns, url
from inTabasco_.apps.inTabasco.views import *

urlpatterns = patterns('',
	url(r'^$', index),
    url(r'^resultado/(?P<buscar>.+)/(?P<categoria>\w+)/(?P<ubicacion>.+)/', resultado),
    url(r'^categoria/(?P<categoria_id>\d+)/', categoria),
    url(r'^detalle/(?P<direccion>.+)/(?P<categoria>\w+)/(?P<espacio_id>\d+)/', detalle),
    url(r'^visitas_espacios/', visitas_espacios),
    url(r'^colonias_cercanas/', colonias_cercanas),
    url(r'^regitro_socio_web/', regitro_socio_web),
    url(r'^busqueda_socio_vip/(?P<nombre>.+)', busqueda_socio_vip),
    url(r'^contactar_socio/(?P<espacio_id>\d+)', contactar_socio),
    url(r'^mis_espacios_web/(?P<socio_id>\d+)', mis_espacios_web),
    url(r'^mensajes/(?P<socio_id>\d+)', mensajes),
    url(r'^detalle_mensaje/(?P<mensaje_id>\d+)', detalle_mensaje),

	)