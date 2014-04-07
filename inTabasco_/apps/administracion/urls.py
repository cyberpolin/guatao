from django.conf.urls import patterns, url
from inTabasco_.apps.administracion.views import *

urlpatterns = patterns('',
	url(r'^principal', principal),
	url(r'^consulta_detalle_agente', consulta_detalle_agente),
	url(r'^agregar_localidad', agregar_localidad),
	url(r'^validar_usuario', validar_usuario),
	url(r'^alta_persona_socio', alta_persona_socio),
	url(r'^editar_socio/(?P<id_socio>\d+)', editar_socio),

	url(r'^consulta_socio_espacio', consulta_socio_espacio),
	url(r'^detalle_socio/(?P<id_socio>\d+)', detalle_socio),
	
	url(r'^alta_espacio_socio/(?P<id_socio>\d+)', alta_espacio_socio),
	url(r'^editar_agente/(?P<id_agente>\d+) and (?P<id_persona>\d+) and (?P<id_direccion>\d+)/', editar_agente),



	
	url(r'^bloquear_agente/(?P<id_agente>\d+)', bloquear_agente),
	url(r'^activar_agente/(?P<id_agente>\d+)', activar_agente),
    url(r'^bloquear_socio/(?P<id_socio>\d+)', bloquear_socio),
	url(r'^activar_socio/(?P<id_socio>\d+)', activar_socio),
	url(r'^ventas_agente/', ventas_agente),
	
	url(r'^borrar_espacio/(?P<id_espacio>\d+) and (?P<id_socio>\d+)', borrar_espacio),
	url(r'^activar_espacio/(?P<id_espacio>\d+) and (?P<id_socio>\d+)', activar_espacio),


	url(r'^control_dinero/', control_dinero),
	url(r'^corte_agente/(?P<id_agente>\d+)', corte_agente),
	url(r'^corte_general_agente', corte_general_agente),
	url(r'^registrar_caja', registrar_caja),	

	
	)