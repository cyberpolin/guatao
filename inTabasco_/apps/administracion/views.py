#encoding:utf-8
from django.http import *
from django.contrib.auth.decorators import * # Libreria para el login required
from django.shortcuts import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from inTabasco_.apps.inTabasco.models import *
import datetime
from datetime import date
from decimal import Decimal
from inTabasco_.apps.administracion.forms import *
from django.contrib import messages
from inTabasco_.apps.inTabasco.forms import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from django.utils import simplejson
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='/login_')
def principal(request):	

	#Lista de Agentes Agente de Ventas
	agentes = agente_ventas.objects.filter(Q(status__status = 'A') | Q(status__status = 'P'))
	agentes_count = agentes.count()
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(agentes, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		agentes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		agentes = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		agentes = paginator.page(paginator.num_pages)

	localidades = cat_localidad.objects.all()
	#AGREGA AGENTE DE VENTAS#
	formulario = UserCreationForm()
	formulario_agente = Registrar_Agente()
	if 'agente' in request.POST:
		formulario_agente = Registrar_Agente(request.POST, request.FILES)
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid() and formulario_agente.is_valid():


			foto = formulario_agente.cleaned_data['foto']
			nombre = formulario_agente.cleaned_data['nombre']
			apellido_paterno = formulario_agente.cleaned_data['apellido_paterno']
			apellido_materno = formulario_agente.cleaned_data['apellido_materno']
			fecha_nacimiento = formulario_agente.cleaned_data['fecha_nacimiento']
			correo = formulario_agente.cleaned_data['correo']
			telefono = formulario_agente.cleaned_data['telefono']
			celular = formulario_agente.cleaned_data['celular']
			tipo_usuario = formulario_agente.cleaned_data['tipo_usuario']

			localidad = formulario_agente.cleaned_data['localidad']
			colonia = formulario_agente.cleaned_data['colonia']
			calle = formulario_agente.cleaned_data['calle']
			numero = formulario_agente.cleaned_data['numero']
			codigo_postal = formulario_agente.cleaned_data['codigo_postal']
			latitud = formulario_agente.cleaned_data['latitud']
			longitud = formulario_agente.cleaned_data['longitud']

			status = formulario_agente.cleaned_data['status']

			usuario_ = formulario.save()
			grupo = Group.objects.get(name='Agente de Ventas')
			grupo.user_set.add(usuario_)

			consulta_usuario = User.objects.all().get(pk = usuario_.id)
			consulta_usuario.first_name = nombre
			consulta_usuario.last_name = str((apellido_paterno+' '+apellido_materno).encode('utf-8'))
			consulta_usuario.email = correo
			consulta_usuario.save()

			persona = cat_persona()
			persona.imagen = foto
			persona.nombre = nombre
			persona.apellido_paterno = apellido_paterno
			persona.apellido_materno = apellido_materno
			persona.fecha_nacimiento = fecha_nacimiento
			persona.correo = correo
			persona.telefono = telefono
			persona.celular = celular
			persona.tipo_usuario = tipo_usuario
			persona.status = status
			persona.usuario = usuario_


			direccion = cat_direcciones()
			direccion.localidad = localidad
			direccion.colonia = colonia
			direccion.calle = calle
			direccion.numero = numero
			direccion.codigo_postal = codigo_postal
			direccion.latitud = latitud
			direccion.longitud = longitud

			padre = request.POST.get('padre')
			consulta_padre = None
			if padre != '':
				consulta_padre = agente_ventas.objects.all().get(nombre__id = padre)
			else:
				pass


			persona.save()
			direccion.save()



			agente = agente_ventas(
				padre = consulta_padre,
				nombre = persona,
				direccion = direccion,
				usuario = usuario_,
				status = status
				)
			agente.save()

			msj = 'EL agente se guardo correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/principal/')

		else:
			msj = 'Error'
			messages.success(request, msj)

	else:
		formulario = UserCreationForm()
		formulario_agente = Registrar_Agente()

	#TERMINA AGREGA AGENTE DE VENTAS#

	contexto = {'principal':'active','filtrado':filtrado,'localidades':localidades,'formulario_agente':formulario_agente,'formulario':formulario, 'agentes':agentes,'agentes_count':agentes_count}

	return render_to_response('administrador/index.html', contexto ,context_instance = RequestContext(request))

@csrf_exempt
def consulta_detalle_agente(request):	

	if request.is_ajax():
		q=request.POST['q']
		if q is not None:

			agente = agente_ventas.objects.filter(pk = q) #CONSULTA PARA LOS AGENTES
			list = [] #CREAMOS UNA LISTA
			for row in agente: #RECORREMOS NUESTRA CONSULTA
				list.append({#ADEFINIMOS EL O LOS CAMPOS QUE DESEAMOS Y LO AGREGAMOS A LA LISTA, ANTES CREADA
							'id':q,
							'imagen':str(row.nombre.imagen),
							'nombre':row.nombre.nombre,
							'apellido_paterno':row.nombre.apellido_paterno,
							'apellido_materno':row.nombre.apellido_materno,
							'fecha_de_alta':str(row.nombre.fecha_registro),
							'fecha_nacimiento':str(row.nombre.fecha_nacimiento),
							'correo':row.nombre.correo,
							'telefono':row.nombre.telefono,
							'celular':row.nombre.celular,
							'localidad':row.direccion.localidad.nombre,
							'colonia':row.direccion.colonia,
							'calle':row.direccion.calle,
							'numero':row.direccion.numero,
							'codigo_postal':row.direccion.codigo_postal
							})

			recipe_list_json = json.dumps(list) #VOLCAMOS LA LISTA COMO JSON

			print recipe_list_json
			print(q)
	return HttpResponse(recipe_list_json,mimetype="application/javascript")

@login_required(login_url='/login_')
@permission_required('inTabasco.change_agente_ventas', raise_exception=True)
def editar_agente(request, id_agente, id_persona, id_direccion):

	consulta_agente = agente_ventas.objects.get(pk = id_agente)
	consulta_persona = cat_persona.objects.get(pk = id_persona)
	consulta_direccion = cat_direcciones.objects.get(pk = id_direccion)

	usuario = User.objects.get( pk = consulta_persona.usuario.id )

	#Cordenadas
	latit = consulta_agente.direccion.latitud
	longi = consulta_agente.direccion.longitud

	if request.method == 'GET':
#		return HttpResponse(consulta_agente.nombre.imagen)
		formulario_agente = Registrar_Agente( initial = {'padre':consulta_agente.padre,
											 'foto':consulta_agente.nombre.imagen,
											 'nombre':consulta_agente.nombre.nombre,
											 'apellido_paterno':consulta_agente.nombre.apellido_paterno,
											 'apellido_materno':consulta_agente.nombre.apellido_materno,
											 'fecha_nacimiento':consulta_agente.nombre.fecha_nacimiento,
											 'correo':consulta_agente.nombre.correo,
											 'telefono':consulta_agente.nombre.telefono,
											 'celular':consulta_agente.nombre.celular,
											 'tipo_usuario':consulta_agente.nombre.tipo_usuario,
											 'localidad':consulta_agente.direccion.localidad,
											 'colonia':consulta_agente.direccion.colonia,
											 'calle':consulta_agente.direccion.calle,
											 'numero':consulta_agente.direccion.numero,
											 'codigo_postal':consulta_agente.direccion.codigo_postal,
											 'latitud':consulta_agente.direccion.latitud,
											 'longitud':consulta_agente.direccion.longitud,
											 'status':consulta_agente.status.status
											 })

		#return HttpResponse(consulta_agente.nombre.tipo_usuario)
	elif request.method == 'POST':
		formulario_agente = Registrar_Agente(request.POST, request.FILES )



		if formulario_agente.is_valid():


			padre = formulario_agente.cleaned_data['padre']
			foto = formulario_agente.cleaned_data['foto']
			nombre = formulario_agente.cleaned_data['nombre']
			apellido_paterno = formulario_agente.cleaned_data['apellido_paterno']
			apellido_materno = formulario_agente.cleaned_data['apellido_materno']
			fecha_nacimiento = formulario_agente.cleaned_data['fecha_nacimiento']
			correo = formulario_agente.cleaned_data['correo']
			telefono = formulario_agente.cleaned_data['telefono']
			celular = formulario_agente.cleaned_data['celular']
			tipo_usuario = formulario_agente.cleaned_data['tipo_usuario']

			localidad = formulario_agente.cleaned_data['localidad']
			colonia = formulario_agente.cleaned_data['colonia']
			calle = formulario_agente.cleaned_data['calle']
			numero = formulario_agente.cleaned_data['numero']
			codigo_postal = formulario_agente.cleaned_data['codigo_postal']
			latitud = formulario_agente.cleaned_data['latitud']
			longitud = formulario_agente.cleaned_data['longitud']

			status = formulario_agente.cleaned_data['status']


			consulta_agente.padre = padre
			consulta_agente.status = status
			if foto:
				consulta_persona.imagen = foto
			consulta_persona.nombre = nombre
			consulta_persona.apellido_paterno = apellido_paterno
			consulta_persona.apellido_materno = apellido_materno
			consulta_persona.fecha_nacimiento = fecha_nacimiento
			consulta_persona.correo = correo
			consulta_persona.telefono = telefono
			consulta_persona.celular = celular
			consulta_persona.tipo_usuario = tipo_usuario
			consulta_persona.status = status


			consulta_direccion.localidad = localidad
			consulta_direccion.colonia = colonia
			consulta_direccion.calle = calle
			consulta_direccion.numero = numero
			consulta_direccion.latitud = latitud
			consulta_direccion.longitud = longitud

			usuario.first_name = nombre
			usuario.last_name = apellido_paterno + apellido_materno
			usuario.email = correo



			consulta_persona.save()
			consulta_direccion.save()
			consulta_agente.save()
			usuario.save()

			msj = 'El contacto'+' '+ str(nombre.encode('utf-8')+' '+apellido_paterno.encode('utf-8')+' '+apellido_materno.encode('utf-8')) +' '+ 'se actualizo correctamente.'
			messages.success(request, msj)
			return HttpResponseRedirect('/principal/')

		else:
			msj = 'Error'
			messages.success(request, msj)
	else:
		formulario_agente = Registrar_Agente()

	contexto = {'principal':'active','formulario_agente': formulario_agente, 'latit':latit, 'longi':longi, 'consulta_persona':consulta_persona}
	return render_to_response('administrador/edit_agente.html',contexto, context_instance = RequestContext(request))


@login_required(login_url='/login_')
@permission_required('inTabasco.add_espacio', raise_exception=True)
def alta_persona_socio(request):
	list_socios = cat_persona.objects.filter( tipo_usuario__tipo = 'Socio')
	socios = list_socios.count()
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(list_socios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		list_socios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		list_socios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		list_socios = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		formulario_socio = UserCreationForm(request.POST)
		formulario_persona_espacio_socio = Registrar_Persona_Socio(request.POST, request.FILES)
		if formulario_socio.is_valid() and formulario_persona_espacio_socio.is_valid():
						#Agregrega Persona#
			foto = formulario_persona_espacio_socio.cleaned_data['foto']
			nombre_propietario = formulario_persona_espacio_socio.cleaned_data['nombre_propietario']
			apellido_paterno = formulario_persona_espacio_socio.cleaned_data['apellido_paterno']
			apellido_materno = formulario_persona_espacio_socio.cleaned_data['apellido_materno']
			fecha_nacimiento = formulario_persona_espacio_socio.cleaned_data['fecha_nacimiento']
			correo = formulario_persona_espacio_socio.cleaned_data['correo']
			telefono = formulario_persona_espacio_socio.cleaned_data['telefono']
			celular = formulario_persona_espacio_socio.cleaned_data['celular']
			red_social = formulario_persona_espacio_socio.cleaned_data['red_social']
			usuario_red_social = formulario_persona_espacio_socio.cleaned_data['usuario_red_social']
			tipo_usuario = formulario_persona_espacio_socio.cleaned_data['tipo_usuario']


			#Guarda el usuario y lo inserta a su respectivo grupo#
			usuario_ = formulario_socio.save()
			grupo = Group.objects.get(name='Socio')
			grupo.user_set.add(usuario_)

			#Edita al usuario para pasarle nombre, apellidos y correo#
			consulta_usuario = User.objects.all().get(pk = usuario_.id)
			consulta_usuario.first_name = nombre_propietario
			consulta_usuario.last_name = str((apellido_paterno+' '+apellido_materno).encode('utf-8'))
			consulta_usuario.email = correo
			consulta_usuario.save()

			persona = cat_persona()
			persona.imagen = foto
			persona.nombre = nombre_propietario
			persona.apellido_paterno = apellido_paterno
			persona.apellido_materno = apellido_materno
			persona.fecha_nacimiento = fecha_nacimiento
			persona.correo = correo
			persona.telefono = telefono
			persona.celular = celular
			persona.red_social = red_social
			persona.nombre_red = usuario_red_social
			persona.tipo_usuario = tipo_usuario
			persona.status_id = 1
			persona.usuario = usuario_
			persona.agente_venta = request.user
			persona.save()

			msj = 'EL Socio se guardo correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/alta_persona_socio/')

		else:
			msj = 'Error'
			messages.success(request, msj)

	else:
		formulario_socio = UserCreationForm()
		formulario_persona_espacio_socio = Registrar_Persona_Socio()
	contexto = {'alta_espacio':'active','filtrado':filtrado,'request':request,'list_socios':list_socios,'socios':socios,'formulario_socio':formulario_socio,'formulario_persona_espacio_socio':formulario_persona_espacio_socio}
	return render_to_response('administrador/agregar_socio_espacio.html', contexto, context_instance = RequestContext(request))





@login_required(login_url='/login_')
@permission_required('inTabasco.add_espacio', raise_exception=True)
def editar_socio(request, id_socio):
	socio = cat_persona.objects.get(pk=id_socio)

	if request.method == 'GET':
#		return HttpResponse(consulta_agente.nombre.imagen)
		formulario_persona_espacio_socio = Registrar_Persona_Socio( initial = {'foto':socio.imagen,
																				'nombre_propietario':socio.nombre,
																				'apellido_paterno':socio.apellido_paterno,
																				'apellido_materno':socio.apellido_materno,
																				'fecha_nacimiento':socio.fecha_nacimiento,
																				'correo':socio.correo,
																				'telefono':socio.telefono,
																				'celular':socio.celular,

																				'tipo_usuario':socio.tipo_usuario,

																				'red_social':socio.red_social,
																				'usuario_red_social':socio.nombre_red})
	elif request.method == 'POST':
		formulario_persona_espacio_socio = Registrar_Persona_Socio(request.POST, request.FILES)
		if formulario_persona_espacio_socio.is_valid():

			foto = formulario_persona_espacio_socio.cleaned_data['foto']
			nombre_propietario = formulario_persona_espacio_socio.cleaned_data['nombre_propietario']
			apellido_paterno = formulario_persona_espacio_socio.cleaned_data['apellido_paterno']
			apellido_materno = formulario_persona_espacio_socio.cleaned_data['apellido_materno']
			fecha_nacimiento = formulario_persona_espacio_socio.cleaned_data['fecha_nacimiento']
			correo = formulario_persona_espacio_socio.cleaned_data['correo']
			telefono = formulario_persona_espacio_socio.cleaned_data['telefono']
			celular = formulario_persona_espacio_socio.cleaned_data['celular']
			tipo_usuario = formulario_persona_espacio_socio.cleaned_data['tipo_usuario']


			red_social = formulario_persona_espacio_socio.cleaned_data['red_social']
			nombre_red = formulario_persona_espacio_socio.cleaned_data['usuario_red_social']

			if foto:
				socio.imagen = foto
			socio.nombre = nombre_propietario
			socio.apellido_paterno = apellido_paterno
			socio.apellido_materno = apellido_materno
			socio.fecha_nacimiento = fecha_nacimiento
			socio.correo = correo
			socio.telefono = telefono
			socio.celular = celular
			socio.red_social = red_social
			socio.nombre_red = nombre_red
			socio.tipo_usuario = tipo_usuario
			socio.save()

			msj = 'EL Socio se edito correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/alta_persona_socio/')



	else:
		formulario_persona_espacio_socio = Registrar_Persona_Socio()

	contexto = {'alta_espacio':'active','request':request,'formulario_persona_espacio_socio':formulario_persona_espacio_socio}
	return render_to_response('administrador/editar_socio.html', contexto, context_instance = RequestContext(request))




@login_required(login_url='/login_')
@permission_required('inTabasco.add_espacio', raise_exception=True)
def alta_espacio_socio(request, id_socio):
	localidades = cat_localidad.objects.all()
	socio = cat_persona.objects.get( pk = id_socio )
	if 'espacio' in request.POST:

		formulario = Registrar_Espacio_Socio(request.POST, request.FILES)
		if formulario.is_valid():

			localidad = formulario.cleaned_data['localidad']
			colonia = formulario.cleaned_data['colonia']
			calle = formulario.cleaned_data['calle']
			numero = formulario.cleaned_data['numero']
			codigo_postal = formulario.cleaned_data['codigo_postal']
			dias_laborales = formulario.cleaned_data['dias_laborales']
			horario_atencion = formulario.cleaned_data['horario_atencion']
			latitud = formulario.cleaned_data['latitud']
			longitud = formulario.cleaned_data['longitud']

			direccion = cat_direcciones()
			direccion.localidad = localidad
			direccion.colonia = colonia
			direccion.calle = calle
			direccion.numero = numero
			direccion.codigo_postal = codigo_postal
			direccion.latitud = latitud
			direccion.longitud = longitud

			direccion.save()

			#Agregar datos a la tabla espacio#
			rfc = formulario.cleaned_data['rfc']
			nombre_establecimiento = formulario.cleaned_data['nombre_establecimiento']
			descripcion_corta = formulario.cleaned_data['descripcion_corta']
			descripcion_larga = formulario.cleaned_data['descripcion_larga']
			url = formulario.cleaned_data['url']
			socio_vip = formulario.cleaned_data['socio_vip']
			producto = formulario.cleaned_data['producto']

			status = formulario.cleaned_data['status']

			persona = cat_persona.objects.get(pk = id_socio)

			espacio_socio = espacio(rfc = rfc,
									nombre = nombre_establecimiento,
									propietario = persona,
									descripcion_corta = descripcion_corta,
									descripcion_larga = descripcion_larga,
									direccion = direccion,
									url = url,
									socio_vip = socio_vip,
									dias_laborales = dias_laborales,
									horario_atencion = horario_atencion,
									usuario = request.user,
									status = status,
									producto = producto
									)
			espacio_socio.save()
			categorias = request.POST.getlist( 'categorias' )
			for p in categorias:
				espacio_socio.categorias.add(p)
				espacio_socio.save()

						#Agrega la imagen del negocio ala tabla Cat_imagenes#
			imagen = formulario.cleaned_data['imagen']
			imagen_espacio = cat_imagenes(imagen = imagen,
											espacio = espacio_socio)
			imagen_espacio.save()

			#Se guarda la tabla de venta#
			ventas = venta(agente = request.user,
							fecha_venta = datetime.now(),
							espacio = espacio_socio,

							)
			ventas.save()

			msj = 'EL espacio se guardo correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/alta_espacio_socio/' + str(id_socio))


		else:
			msj = 'Error'
			messages.success(request, msj)

	else:
		formulario = Registrar_Espacio_Socio()

	contexto = {'localidades':localidades,'socio':socio,'formulario_espacio':formulario}
	return render_to_response('administrador/alta_espacio_socio.html', contexto, context_instance = RequestContext(request))


@login_required(login_url='/login_')
@permission_required('inTabasco.add_espacio', raise_exception=True)
def editar_espacio_socio(request, id_espacio):


	imagen_espacio = cat_imagenes.objects.get( espacio = id_espacio )
	edi_espacio = espacio.objects.get( pk = id_espacio )
	direccion = cat_direcciones.objects.get( pk = edi_espacio.direccion.id )
	#return HttpResponse(imagen_espacio.imagen)
	if request.method == 'GET':
		formulario = Registrar_Espacio_Socio( initial = {
														'imagen':imagen_espacio.imagen,
														'rfc':edi_espacio.rfc,
														'nombre_establecimiento':edi_espacio.nombre,
														'descripcion_corta':edi_espacio.descripcion_corta,
														'descripcion_larga':edi_espacio.descripcion_larga,
														'categorias':edi_espacio.categorias.all(),
														'socio_vip':edi_espacio.socio_vip,
														'localidad':direccion.localidad,
														'colonia':direccion.colonia,
														'calle':direccion.calle,
														'numero':direccion.numero,
														'codigo_postal':direccion.codigo_postal,
														'latitud':direccion.latitud,
														'longitud':direccion.longitud,
														'dias_laborales':edi_espacio.dias_laborales,
														'horario_atencion':edi_espacio.horario_atencion,
														'status':edi_espacio.status,
														'url':edi_espacio.url,
														'producto':edi_espacio.producto,
														})
	elif 'espacio' in request.POST:

		formulario = Registrar_Espacio_Socio(request.POST, request.FILES)

		if formulario.is_valid():
						#Agrega Direccion#
			localidad = formulario.cleaned_data['localidad']
			colonia = formulario.cleaned_data['colonia']
			calle = formulario.cleaned_data['calle']
			numero = formulario.cleaned_data['numero']
			codigo_postal = formulario.cleaned_data['codigo_postal']
			dias_laborales = formulario.cleaned_data['dias_laborales']
			horario_atencion = formulario.cleaned_data['horario_atencion']
			latitud = formulario.cleaned_data['latitud']
			longitud = formulario.cleaned_data['longitud']


			direccion.localidad = localidad
			direccion.colonia = colonia
			direccion.calle = calle
			direccion.numero = numero
			direccion.codigo_postal = codigo_postal
			direccion.latitud = latitud
			direccion.longitud = longitud

			direccion.save()

			#Agregar datos a la tabla espacio#
			rfc = formulario.cleaned_data['rfc']
			nombre_establecimiento = formulario.cleaned_data['nombre_establecimiento']
			descripcion_corta = formulario.cleaned_data['descripcion_corta']
			descripcion_larga = formulario.cleaned_data['descripcion_larga']
			url = formulario.cleaned_data['url']
			socio_vip = formulario.cleaned_data['socio_vip']


			edi_espacio.rfc = rfc
			edi_espacio.nombre = nombre_establecimiento
			edi_espacio.descripcion_corta = descripcion_corta
			edi_espacio.descripcion_larga = descripcion_larga
			edi_espacio.url = url
			edi_espacio.socio_vip = socio_vip
			edi_espacio.dias_laborales = dias_laborales
			edi_espacio.horario_atencion = horario_atencion
			edi_espacio.save()


			categorias = edi_espacio.categorias.all()
			for categoria in categorias:
				edi_espacio.categorias.remove(categoria.id)

			categorias = request.POST.getlist( 'categorias' )
			for p in categorias:
				edi_espacio.categorias.add(p)
				edi_espacio.save()



						#Agrega la imagen del negocio ala tabla Cat_imagenes#
			imagen = formulario.cleaned_data['imagen']
			if imagen:
				imagen_espacio.imagen = imagen
				imagen_espacio.save()


			msj = 'EL espacio se guardo correctamente'
			messages.success(request, msj)
			return HttpResponse('Editado correctamente')


		else:
			msj = 'Error'
			messages.success(request, msj)

	else:
		formulario = Registrar_Espacio_Socio()

	contexto = {'formulario_espacio':formulario,'edi_espacio':edi_espacio}
	return render_to_response('administrador/editar_espacio_socio.html', contexto, context_instance = RequestContext(request))


@csrf_exempt
def consulta_socio_espacio(request):	
	results=""
	if request.is_ajax():
		q=request.POST['q']
		print q
		if q is not None:


			list=[]
			obj1 = cat_persona.objects.filter(id = q)

			for row in obj1:#RECORREMOS NUESTRA CONSULTA
				list.append({#ADEFINIMOS EL O LOS CAMPOS QUE DESEAMOS Y LO AGREGAMOS A LA LISTA, ANTES CREADA
							'imagen':str(row.imagen.name),
							'nombre':row.nombre,
							'apellido_paterno':row.apellido_paterno,
							'apellido_materno':row.apellido_materno,
							'fecha_registro':str(row.fecha_registro),
							'fecha_nacimiento':str(row.fecha_nacimiento),
							'correo':row.correo,
							'telefono':row.telefono,
							'celular':row.celular,
							'id':row.id
							})

			recipe_list_json = json.dumps(list)
			print recipe_list_json

	return HttpResponse(recipe_list_json,mimetype="application/javascript")


@login_required(login_url='/login_')
@permission_required('inTabasco.consulta_espacio', raise_exception = True )
def detalle_socio( request, id_socio ):
	socio = cat_persona.objects.get( pk = id_socio )
	list_espacios = espacio.objects.filter( propietario = id_socio )

	contexto = {'alta_espacio':'active','socio':socio, 'list_espacios':list_espacios }
	return render_to_response('administrador/detalle_socio.html', contexto, context_instance = RequestContext(request))


@csrf_exempt
@login_required(login_url='/login_')
@permission_required('inTabasco.add_cat_localidad', raise_exception = True)
def agregar_localidad(request):
	if request.is_ajax():
		try:
			idi = request.POST['padre']
		except:
			idi=None

		try:
			local = cat_localidad.objects.get(pk=idi)
		except cat_localidad.DoesNotExist:
			local = None

		nombre = request.POST['localidad_direccion']

		padre = local

		localidades = cat_localidad()
		localidades.padre = padre
		localidades.nombre = nombre

		localidades.save()

		mensaje = {"estatus":"True", "nombre":localidades.nombre, "id_localidad":localidades.id}
		#messages.success(request, 'Beneficiario registrado')
		#print mensaje
		return HttpResponse(simplejson.dumps(mensaje),mimetype="application/json")

@csrf_exempt
def validar_usuario(request):	
	results=""
	if request.is_ajax():
		q=request.POST['q']
		#q = request.GET.get( 'q' )
		if q is not None:
			results = User.objects.filter(username= q).order_by( 'username' )

	return render_to_response('administrador/validar_usuario.html',{'results':results},context_instance = RequestContext( request ) )


@login_required(login_url='/login_')
@permission_required('inTabasco.delete_agente_ventas', raise_exception=True)
def bloquear_agente(request, id_agente):
	agente = agente_ventas.objects.all().get( pk = id_agente )
	agente.status = cat_status.objects.all().get( status = 'I')
	persona_agente = cat_persona.objects.get( pk = agente.nombre.id )
	persona_agente.status = cat_status.objects.all().get( status = 'I')
	persona_agente.save()

	usuario = User.objects.get(pk = agente.usuario.id)
	usuario.is_active = False
	usuario.save()
	agente.save()

	return  HttpResponseRedirect( '/principal/' )

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_agente_ventas', raise_exception=True)
def activar_agente(request, id_agente):

	agente = agente_ventas.objects.all().get( pk = id_agente )
	agente.status = cat_status.objects.all().get( status = 'A')
	persona_agente = cat_persona.objects.get( pk = agente.nombre.id )
	persona_agente.status = cat_status.objects.all().get( status = 'A')
	persona_agente.save()
	usuario = User.objects.get(pk = agente.usuario.id)
	usuario.is_active = True
	usuario.save()
	agente.save()

	return  HttpResponseRedirect( '/principal/' )

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_agente_ventas', raise_exception=True)
def bloquear_socio(request, id_socio):

	socio = cat_persona.objects.get( pk = id_socio )
	socio.status = cat_status.objects.all().get( status = 'I')
	socio.save()

	usuario = User.objects.get(pk = socio.usuario.id)
	usuario.is_active = False
	usuario.save()

	return  HttpResponseRedirect( '/alta_persona_socio/' )

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_agente_ventas', raise_exception=True)
def activar_socio(request, id_socio):

	socio = cat_persona.objects.get( pk = id_socio )
	socio.status = cat_status.objects.all().get( status = 'A')
	socio.save()
	usuario = User.objects.get(pk = socio.usuario.id)
	usuario.is_active = True
	usuario.save()


	return  HttpResponseRedirect( '/alta_persona_socio/' )



@login_required(login_url='/login_')
@permission_required('inTabasco.delete_espacio', raise_exception = True )
def borrar_espacio(request, id_espacio, id_socio):

	espacio_ = espacio.objects.all().get( pk = id_espacio )
	espacio_.status = cat_status.objects.all().get( status = 'I')
	espacio_.save()

	return  HttpResponseRedirect( '/detalle_socio/'+str(id_socio) )

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_espacio', raise_exception = True )
def activar_espacio(request, id_espacio, id_socio):

	espacio_ = espacio.objects.all().get( pk = id_espacio )
	espacio_.status = cat_status.objects.all().get( status = 'A')
	espacio_.save()

	return  HttpResponseRedirect( '/detalle_socio/'+str(id_socio) )

@login_required(login_url='/login_')
def agentes_eliminados( request ):

	eliminados = agente_ventas.objects.filter( status__status = 'I')
	cantidad_eliminados = eliminados.count
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(eliminados, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		eliminados = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		eliminados = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		eliminados = paginator.page(paginator.num_pages)
	contexto = {'filtrado':filtrado,'agentes_eliminados':'active','eliminados':eliminados,'cantidad_eliminados':cantidad_eliminados,'agentes_eliminados':'active'}
	return render_to_response('administrador/agentes_eliminados.html',contexto,context_instance = RequestContext(request))

@csrf_exempt
@login_required(login_url='/login_')
@permission_required('inTabasco.consulta_venta', raise_exception = True )
def control_dinero(request):

	if request.is_ajax():

		fecha = request.POST.get('fecha')

		d = date.today()
		if fecha == 'dia' :
			ventas_dia = venta.objects.filter( fecha_venta = d ).exclude(espacio__producto__precio__pk = 2)
			total_ventas_dia = ventas_dia.count()

			total_precio_dia = 0
			list = []
			for ventas in ventas_dia:
				total_precio_dia = (Decimal(str(total_precio_dia))) + ((Decimal(str(ventas.espacio.producto.precio)) - 200))

			list.append({
						'total_ventas_dia':total_ventas_dia,
						'total_precio_dia':str(total_precio_dia)
						})

			recipe_list_json = json.dumps(list)

		if fecha == 'mes':
			mes = d.month
			ventas_mes = venta.objects.filter( fecha_venta__month = mes ).exclude(espacio__producto__precio__pk = 2)
			total_ventas_mes = ventas_mes.count()


			total_precio_mes = 0
			list = []
			for ventas in ventas_mes:
				total_precio_mes = (Decimal(str(total_precio_mes))) + ((Decimal(str(ventas.espacio.producto.precio)) - 200 ))

			list.append({
						'total_ventas_mes':total_ventas_mes,
						'total_precio_mes':str(total_precio_mes)
						})

			recipe_list_json = json.dumps(list)

		if fecha == 'ano':
			ano = d.year
			ventas_ano = venta.objects.filter( fecha_venta__year = ano ).exclude(espacio__producto__precio__pk = 2)
			total_ventas_ano = ventas_ano.count()


			total_precio_ano = 0
			list = []
			for ventas in ventas_ano:
				total_precio_ano = (Decimal(str(total_precio_ano))) + ((Decimal(str(ventas.espacio.producto.precio)) - 200 ))

			list.append({
						'total_ventas_ano':total_ventas_ano,
						'total_precio_ano':str(total_precio_ano)
						})

			recipe_list_json = json.dumps(list)

		if fecha == 'total':

			ventas = venta.objects.filter( ).exclude(espacio__producto__precio__pk = 2)
			total_ventas = ventas.count()


			total_precio = 0
			list = []
			for ventas in ventas:
				total_precio = (Decimal(str(total_precio))) + ((Decimal(str(ventas.espacio.producto.precio)) - 200 ))

			list.append({
						'total_ventas':total_ventas,
						'total_precio':str(total_precio)
						})

			recipe_list_json = json.dumps(list)
			print recipe_list_json
	return HttpResponse(recipe_list_json,mimetype="application/javascript")



@csrf_exempt	
@login_required(login_url='/login_')
@permission_required('inTabasco.consulta_venta', raise_exception = True )
def ventas_agente(request):

	agente_id = request.POST.get('q')
	d = date.today()

	ventas = venta.objects.filter(agente__id = agente_id, fecha_venta = d)
	contador = ventas.count()

	precio = 0
	for p in ventas:
		precio = p.espacio.producto.precio


	pago_inTabasco = ((Decimal(str(precio)) - 200)) * contador
	pago_agente_ventas = (Decimal(str(precio)) - 300) * contador


	total = Decimal(str(precio)) * contador

	list = []

	list.append({
				'contador':str(contador),
				'total':str(total),
				'pago_inTabasco':str(pago_inTabasco),
				'pago_agente_ventas':str(pago_agente_ventas),
				})

	recipe_list_json = json.dumps(list)
	return HttpResponse(recipe_list_json, mimetype="application/javascript")


@login_required(login_url='/login_')
@permission_required('inTabasco.corte_agente', raise_exception = True )
def corte_agente(request, id_agente):
	agente = agente_ventas.objects.all().get( pk = id_agente )
	agente.status = cat_status.objects.all().get( status = 'P')
	agente.save()

	return  HttpResponseRedirect( '/principal/' )

@login_required(login_url='/login_')
@permission_required('inTabasco.corte_agente', raise_exception = True )
def corte_general_agente(request):	
	agentes_A = agente_ventas.objects.all().filter(status__status = 'A')

	usuario_id = ''
	for a in agentes_A:
		a.status = cat_status.objects.all().get( status = 'I')
		a.usuario.is_active = False
		a.save()
		usuario_id = a.usuario.id
		usuario = User.objects.filter(pk = usuario_id)

		for x in usuario:
			x.is_active = False
			x.save()

	agentes_P = agente_ventas.objects.all().filter(status__status = 'P')
	for p in agentes_P:
		p.status = cat_status.objects.all().get( status = 'A')
		p.save()


	return  HttpResponseRedirect( '/principal/' )


@login_required(login_url='/login_')
@permission_required('inTabasco.add_caja', raise_exception = True )
def registrar_caja(request):
	if request.method == 'POST':
		formulario = Registro_Movimiento_Caja(request.POST)
		if formulario.is_valid():

			movimiento = formulario.cleaned_data['tipo_movimiento']
			descripcion = formulario.cleaned_data['descripcion']
			cantidad = formulario.cleaned_data['cantidad']
			fecha = formulario.cleaned_data['fecha']


			tipo_movimiento = cat_tipo_movimiento.objects.all().get( movimiento = movimiento )



			registrar = caja()
			registrar.movimiento = tipo_movimiento
			registrar.descripcion = descripcion
			registrar.cantidad = cantidad
			registrar.fecha = fecha

			registrar.save()

			msj = 'EL movimiento se registro correctamente'
			messages.success(request, msj)
			HttpResponseRedirect('/caja/')

		else:
			msj = 'Error'
			messages.success(request, msj)

	else:
		formulario = Registro_Movimiento_Caja()
	contexto = {'formulario':formulario}
	return render_to_response('caja.html', contexto, context_instance = RequestContext(request))

@login_required(login_url='/login_')
def buscar_persona(request, persona, tipo_usuario, status):
	persona_socio = None
	principal = None
	agentes_eliminados = None
	alta_espacio = None
	persona_agente = None
	if (tipo_usuario == 'Agente'):

		if status == 'A':
			principal = 'active'
		else:
			agentes_eliminados = 'active'

		persona_agente = agente_ventas.objects.filter((Q( nombre__nombre__icontains = persona) | Q( nombre__apellido_paterno__icontains = persona)| Q( nombre__apellido_materno__icontains = persona)), nombre__tipo_usuario__tipo = tipo_usuario, status__status = status)
		filtrado = 5 # Show 10 contacts per page
		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(persona_agente, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')

		try:
			persona_agente = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			persona_agente = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			persona_agente = paginator.page(paginator.num_pages)


	elif (tipo_usuario == "Socio"):
		alta_espacio ='active'

		persona_socio = cat_persona.objects.filter((Q( nombre__icontains = persona) | Q( apellido_paterno__icontains = persona)| Q( apellido_materno__icontains = persona)), tipo_usuario__tipo = tipo_usuario, status__status = status)

		filtrado = 5 # Show 10 contacts per page
		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(persona_socio, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')
		try:
			persona_socio = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			persona_socio = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			persona_socio = paginator.page(paginator.num_pages)

	contexto = {'persona_agente':persona_agente,'persona_socio':persona_socio,'filtrado':filtrado,'principal':principal,'alta_espacio':alta_espacio,'agentes_eliminados':agentes_eliminados}
	return render_to_response('administrador/resultado_busqueda_persona.html',contexto, context_instance = RequestContext(request))

@login_required(login_url='/login_')
def lista_espacios( request ):
	list_espacios = espacio.objects.filter( status__status = 'A')
	cantidad_espacios = list_espacios.count()
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(list_espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')
	try:
		list_espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		list_espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		list_espacios = paginator.page(paginator.num_pages)
	contexto = {'list_espacios':list_espacios,'lista_espacios':'active','cantidad_espacios':cantidad_espacios,'filtrado':filtrado}
	return render_to_response('administrador/lista_espacios.html', contexto, context_instance = RequestContext(request))

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_espacio', raise_exception = True )
def lista_borrar_espacio(request, id_espacio):

	espacio_ = espacio.objects.all().get( pk = id_espacio )
	espacio_.status = cat_status.objects.all().get( status = 'I')
	espacio_.save()

	return  HttpResponseRedirect( '/lista_espacios/' )

@login_required(login_url='/login_')
@permission_required('inTabasco.delete_espacio', raise_exception = True )
def lista_activar_espacio(request, id_espacio):

	espacio_ = espacio.objects.all().get( pk = id_espacio )
	espacio_.status = cat_status.objects.all().get( status = 'A')
	espacio_.save()

	return  HttpResponseRedirect( '/lista_espacios/')

@login_required(login_url='/login_')
def buscar_espacio(request, nombre_espacio, status):
	lista_espacios = None
	espacios_eliminados = None
	if status == 'A':
		lista_espacios='active'
	else:
		espacios_eliminados='active'
	list_espacios = espacio.objects.filter( nombre__icontains = nombre_espacio, status__status = status)
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(list_espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')
	try:
		list_espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		list_espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		list_espacios = paginator.page(paginator.num_pages)
	contexto = {'list_espacios':list_espacios,'lista_espacios':lista_espacios,'espacios_eliminados':espacios_eliminados,'filtrado':filtrado}
	return render_to_response('administrador/resultado_busqueda_espacios.html',contexto, context_instance = RequestContext( request ))

@login_required(login_url='/login_')
def espacios_eliminados( request ):
	list_espacios = espacio.objects.filter( status__status = 'I')
	cantidad_espacios = list_espacios.count()
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(list_espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')
	try:
		list_espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		list_espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		list_espacios = paginator.page(paginator.num_pages)
	contexto = {'list_espacios':list_espacios,'espacios_eliminados':'active','cantidad_espacios':cantidad_espacios,'filtrado':filtrado}
	return render_to_response('administrador/espacios_eliminados.html', contexto, context_instance = RequestContext(request))


@login_required(login_url='/login_')
def registrar_categoria( request ):
	categorias = cat_categorias_espacios.objects.all()
	categorias_count = categorias.count
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(categorias, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')
	try:
		categorias = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		categorias = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		categorias = paginator.page(paginator.num_pages)
	if request.method == 'POST':
		formulario = Registrar_Categoria( request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			msj = 'La categoria se registro correctamente.'
			messages.success( request, msj )
			return HttpResponseRedirect( '/registrar_categoria/' )
		else:
			msj = 'Error'
			messages.error( request, msj )
	else:
		formulario = Registrar_Categoria()

	contexto = {'filtrado':filtrado,'categorias':categorias,'categorias_count':categorias_count,'formulario':formulario,'agregar_categorias':'active'}
	return render_to_response('administrador/registrar_categoria.html', contexto ,context_instance = RequestContext(request))


@login_required(login_url='/login_')
def borrar_categoria( request, id_categoria):
	categoria = cat_categorias_espacios.objects.get( pk = id_categoria )
	categoria.delete()
	return HttpResponseRedirect('/registrar_categoria/')

@login_required(login_url='/login')
def editar_categoria( request, id_categoria ):
	categorias = cat_categorias_espacios.objects.all()
	categorias_count = categorias.count
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(categorias, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')
	try:
		categorias = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		categorias = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		categorias = paginator.page(paginator.num_pages)

	categoria_editar = cat_categorias_espacios.objects.get( pk = id_categoria )


	if request.method == 'GET':
		formulario = Registrar_Categoria( instance = categoria_editar)

	elif request.method == 'POST':
		formulario = Registrar_Categoria( request.POST,request.FILES, instance = categoria_editar )
		if formulario.is_valid():

			formulario.save()
			msj = 'La categoria se edito correctamente.'
			messages.success( request, msj )
			return HttpResponseRedirect( '/registrar_categoria/' )
		else:
			msj = 'Error'
			messages.error( request, msj )
	else:
		formulario = Registrar_Categoria()

	contexto = {'filtrado':filtrado,'categoria_editar':categoria_editar,'categorias':categorias,'categorias_count':categorias_count,'formulario':formulario,'agregar_categorias':'active'}
	return render_to_response('administrador/registrar_categoria.html', contexto ,context_instance = RequestContext(request))
