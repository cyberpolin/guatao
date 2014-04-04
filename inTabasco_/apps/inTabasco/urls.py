from django.conf.urls import patterns, url
from inTabasco_.apps.inTabasco.views import *

urlpatterns = patterns('',
	url(r'^$', index),
    url(r'^resultado/(?P<buscar>.+)/(?P<categoria>\w+)/(?P<ubicacion>.+)/', resultado),
    url(r'^categoria/(?P<categoria_id>\d+)/', categoria),
    url(r'^detalle/(?P<direccion>.+)/(?P<categoria>.+)/(?P<espacio_id>\d+)/', detalle),
    url(r'^visitas_espacios/', visitas_espacios),
    url(r'^colonias_cercanas/', colonias_cercanas),
    url(r'^regitro_socio_web/', regitro_socio_web),
    url(r'^busqueda_socio_vip/(?P<nombre>.+)', busqueda_socio_vip),
    url(r'^contactar_socio/(?P<espacio_id>\d+)', contactar_socio),
    url(r'^mis_espacios_web/(?P<socio_id>\d+)', mis_espacios_web),
    url(r'^mensajes/(?P<socio_id>\d+)', mensajes),
    url(r'^detalle_mensaje/(?P<mensaje_id>\d+)', detalle_mensaje),
    url(r'^perfil_socio/(?P<socio_id>\d+)', perfil_socio),
    url(r'^localidades_cercanas/(?P<colonia>.+)/', localidades_cercanas),



    url(r'^cambio_password/chpasswd/done/?',
    'django.contrib.auth.views.password_change_done',
    {'template_name':'registration/password_change_done.html'}),

    url(r'^cambio_password/chpasswd/?','django.contrib.auth.views.password_change',
    {'template_name':'registration/password_change_form.html'}),


	)