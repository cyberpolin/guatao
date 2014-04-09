#encoding:utf-8
from django.http import *
from django.contrib.auth.decorators import * # Libreria para el login required
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from inTabasco_.apps.inTabasco.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import *
from django.contrib.auth.decorators import login_required

def index(request):
	categorias = cat_categorias_espacios.objects.all()

	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	total_espacios = espacio.objects.all().count()
	espacios_mas_visto = espacio.objects.filter(status__status = 'A').order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter( espacio__status__status = 'A').order_by('calificacion')[:3]

	contexto = {'espacios_recomendados':espacios_recomendados,'categorias':categorias,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip, 'total_espacios':total_espacios,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/index.html', contexto, context_instance = RequestContext( request ))

def resultado( request, buscar, categoria, ubicacion ):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto = espacio.objects.filter( status__status = 'A').order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]
	espacios = None

	filtrado = 5
	if (buscar != '0' and ubicacion == '0' and categoria == '0'):
		espacios = espacio.objects.filter(nombre__icontains = buscar, status__status = 'A' ).order_by('-num_visitas')
		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')

		try:
			espacios = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			espacios = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			espacios = paginator.page(paginator.num_pages)
		#return  HttpResponse(espacios)

	elif (buscar == '0' and ubicacion == '0' and categoria != '0'):

		espacios = espacio.objects.filter( categorias__categoria__icontains = categoria, status__status = 'A' ).order_by('-num_visitas')

		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')

		try:
			espacios = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			espacios = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			espacios = paginator.page(paginator.num_pages)
			#return  HttpResponse(espacios)

	elif (buscar != '0' and ubicacion != '0' and categoria == '0'):
		espacios = []

		esp = espacio.objects.filter( direccion__localidad__nombre__icontains = ubicacion, nombre__icontains = buscar, status__status = 'A' ).order_by('-num_visitas')
		for e in esp:
			espacios.append(e)
		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')

		try:
			espacios = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			espacios = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			espacios = paginator.page(paginator.num_pages)
		#return  HttpResponse(espacios)

	elif (buscar != '0' and ubicacion != '0' and categoria != '0'):
		tabasco = cat_localidad.objects.get(nombre__iexact=ubicacion)
		espacios = []

		for localidad in tabasco.cat_localidad_set.all():
			esp = espacio.objects.filter( direccion__localidad__nombre__icontains=localidad.nombre, nombre__icontains = buscar, categorias__categoria__icontains = categoria, status__status = 'A' ).order_by('-num_visitas')
			for e in esp:
				espacios.append(e)

		if 'filtrado' in request.GET:
			filtrado = request.GET.get('filtrado')
		paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
		page = request.GET.get('page')

		try:
			espacios = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			espacios = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			espacios = paginator.page(paginator.num_pages)


	contexto = {'espacios_recomendados':espacios_recomendados,'filtrado':filtrado,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacios':espacios, 'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/resultado.html',contexto, context_instance = RequestContext( request ))

def busqueda_socio_vip( request, nombre):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	espacios = espacio.objects.filter(nombre__icontains = nombre, status__status = 'A' ).order_by('-num_visitas')

	contexto = {'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacios':espacios,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/resultado.html',contexto, context_instance = RequestContext( request ))


def categoria( request, categoria_id):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A').order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	espacios = espacio.objects.filter( categorias__id = categoria_id, status__status = 'A' ).order_by('-num_visitas')
	categoria = cat_categorias_espacios.objects.get( pk = categoria_id)

	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		espacios = paginator.page(paginator.num_pages)

	contexto = {'espacios_recomendados':espacios_recomendados,'filtrado':filtrado,'categoria':categoria,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacios':espacios,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/resultado.html',contexto, context_instance = RequestContext( request ))


def detalle( request, espacio_id, categoria, direccion):

	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	detalleEspacio = espacio.objects.get( pk = espacio_id, status__status = 'A' )
	espacios_mas_visto  = espacio.objects.filter(status__status = 'A').order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]
	try:
		categoria_ = cat_categorias_espacios.objects.get( categoria = categoria )
	except cat_categorias_espacios.DoesNotExist:
		categoria_ = None

	if request.method == 'POST':
		formulario = recomendacion_form( request.POST )
		if formulario.is_valid():
			recomiendame = formulario.save( commit = False )
			espacio_  = espacio.objects.get( pk = espacio_id)
			recomiendame.espacio = espacio_
			#return HttpResponse(categoria)
			recomiendame.save()
			msj = 'Tu recomendacion se ha enviado correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/detalle/'+str(direccion)+'/'+categoria+'/'+str(espacio_id)+'/')
		else:
			msj='Error'
			messages.success(request, msj)
	else:
		formulario = recomendacion_form()

	recomendacion = recomendaciones.objects.filter( espacio = espacio_id ).order_by('-fecha')[:10]

	contexto = {'espacios_recomendados':espacios_recomendados,'recomendacion':recomendacion,'formulario':formulario,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacio_':detalleEspacio, 'espacio_id':espacio_id,'espacios_mas_visto':espacios_mas_visto,'direccion':direccion,'categoria':categoria_}
	return render_to_response('web/detalle.html',contexto, context_instance = RequestContext( request ))

@csrf_exempt
def visitas_espacios( request ):
	if request.is_ajax():
		q=request.POST['q']
		if q is not None:

			detalleEspacio = espacio.objects.get( pk = q )
			detalleEspacio.num_visitas +=1
			detalleEspacio.save()

	return HttpResponse(mimetype="application/javascript")

import json
@csrf_exempt
def colonias_cercanas( request ):
	if request.is_ajax():
		lat=request.POST['latitud']
		lon=request.POST['longitud']

		lat_izquierda = float(lat) + 0.007978
		lat_derecha = float(lat) - 0.004257
		lon_derecha = float(lon) + 0.00535
		lon_izquierda = float(lon) - 0.006495

		print(lat)
		print(lon)
		colonias = cat_direcciones.objects.filter( latitud__range = (lat_derecha,lat_izquierda), longitud__range = (lon_derecha, lon_izquierda))
		list = []
		for p in colonias:
			list.append({
						'colonia':p.colonia,
						})
		recipe_list_json = json.dumps(list) #VOLCAMOS LA LISTA COMO JSON

		print (recipe_list_json)


	return HttpResponse((recipe_list_json),mimetype="application/javascript")

def regitro_socio_web( request ):
	if request.method == 'POST':
		formulario = regitro_socio_web_form( request.POST, request.FILES)
		formulario_user = UserCreationForm( request.POST )
		if formulario.is_valid() and formulario_user.is_valid():
			usuario = formulario_user.save()
			usuario.first_name = request.POST.get('nombre')
			usuario.last_name = request.POST.get('apellido_paterno')+' '+request.POST.get('apellido_materno')
			usuario.email = request.POST.get('correo')
			usuario.save()
			grupo = Group.objects.get(name='Socio')
			grupo.user_set.add(usuario)
			socio = formulario.save( commit = False )
			socio.status_id = 1
			socio.usuario = usuario
			socio.save()

			msj = 'EL REGISTRO DEL SOCIO SE REALIZO CORRECTAMENTE'
			messages.success(request, msj)
			return HttpResponseRedirect('/regitro_socio_web/')
		else:
			msj = 'ERROR'
			messages.success( request, msj)
	else:
		formulario = regitro_socio_web_form()
		formulario_user = UserCreationForm()
	contexto={'formulario':formulario,'formulario_user':formulario_user}
	return render_to_response('web/regitro_socio_web.html',contexto, context_instance = RequestContext( request ))

from django.core.mail import EmailMultiAlternatives
def contactar_socio( request, espacio_id ):
	if request.method == 'POST':
		formulario = contactar_socio_form( request.POST )
		if formulario.is_valid():
			espacio_persona = espacio.objects.get(pk = espacio_id)
			persona_contactar = espacio_persona.propietario
			contactar = contactame()
			contactar.nombre = request.POST.get('nombre')
			contactar.correo = request.POST.get('correo')
			contactar.telefono = request.POST.get('telefono')
			contactar.asunto = request.POST.get('asunto')
			contactar.comentario = request.POST.get('comentario')
			contactar.socio_contactar = persona_contactar
			contactar.save()

			correo_socio = espacio_persona.propietario.correo
			text_content = ''
			msj = str('<p><strong>¡Buen dia!.</strong> Un usuario a solicitado informacion de su negocio. Para verlo haz click en el siguiente enlace: <a href="guatao.com.mx/mensajes/'+str(espacio_persona.propietario.usuario.id)+'">guatao.com.mx/mensajes/'+str(espacio_persona.propietario.usuario.id)+'</a></p>')
			subject, from_email, to = 'Nuevo mensaje en guatao.com.mx', 'guatao.com.mx@gmail.com', str(correo_socio)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(msj, "text/html")
			msg.send()
			msj = 'El mensaje se a enviado en seguida me pondre en contacto con usted'
			messages.success( request, msj)
			return HttpResponseRedirect('/contactar_socio/'+espacio_id)


		else:
			msj = 'Error'
			messages.success( request, msj)
	else:
		formulario = contactar_socio_form()

	contexto={'formulario':formulario, 'espacio_id':espacio_id}
	return render_to_response('web/contactar_socio.html',contexto, context_instance = RequestContext( request ))

@login_required(login_url='/login_')
def mis_espacios_web( request, socio_id ):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]



	espacios = espacio.objects.filter( propietario__usuario__id = socio_id, status__status = 'A' ).order_by('-num_visitas')
	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		espacios = paginator.page(paginator.num_pages)

	contexto = {'filtrado':filtrado,'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacios':espacios,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/resultado.html',contexto, context_instance = RequestContext( request ))

@login_required(login_url='/login_')
def mensajes(request, socio_id):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	persona = cat_persona.objects.get( usuario = socio_id)
	mensajes = contactame.objects.filter( socio_contactar = persona).order_by('fecha_mensaje')


	contexto = {'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'mensajes':mensajes,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/mensajes.html',contexto, context_instance = RequestContext( request ))


@login_required(login_url='/login_')
def detalle_mensaje(request, mensaje_id):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	mensaje = contactame.objects.get( pk = mensaje_id)
	mensaje.leido = True
	mensaje.save()

	contexto = {'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'mensaje':mensaje,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/detalle_mensaje.html',contexto, context_instance = RequestContext( request ))

@login_required(login_url='/login_')
def perfil_socio( request, socio_id ):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	persona = cat_persona.objects.get( usuario__id = socio_id )


	contexto = {'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'persona':persona,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/perfil.html',contexto, context_instance = RequestContext( request ))

@login_required(login_url='/login_')
def editar_perfil( request, socio_id):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter( espacio__status__status = 'A' ).order_by('calificacion')[:3]
	socio = cat_persona.objects.get( id = socio_id )

	#usuario_red = usr_redes_sociales.objects.get( usuario__id=socio_id)
	if request.method == 'GET':
		formulario = regitro_socio_web_form( instance = socio )
	elif request.method == 'POST':
		formulario = regitro_socio_web_form(request.POST, request.FILES, instance = socio)
		if formulario.is_valid():
			usuario = User.objects.get( pk = socio.usuario.id)
			usuario.first_name = request.POST.get('nombre')
			usuario.last_name = request.POST.get('apellido_paterno')+' '+request.POST.get('apellido_materno')
			usuario.email = request.POST.get('correo')
			formulario.save()
			usuario.save()

			msj = 'EL perfil se edito correctamente'
			messages.success(request, msj)
			return HttpResponseRedirect('/perfil_socio/'+str(int(socio.usuario.id)))

		else:
			msj = 'Error'
			messages.success( request, msj)



	else:
		formulario = regitro_socio_web_form()


	contexto = {'formulario':formulario,'espacios_recomendados':espacios_recomendados,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'persona':socio,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/editar_perfil.html',contexto, context_instance = RequestContext( request ))


def localidades_cercanas( request, colonia):
	nuevos_socios = espacio.objects.filter( status__status = 'A' ).order_by('-id')[:2]
	socios_vip = espacio.objects.filter( socio_vip = True, status__status = 'A' ).order_by('-id')[:4]
	espacios_mas_visto  = espacio.objects.filter( status__status = 'A' ).order_by('-num_visitas')[:4]
	espacios_recomendados = recomendaciones.objects.filter(espacio__status__status = 'A').order_by('calificacion')[:3]

	espacios = espacio.objects.filter( direccion__colonia = colonia, status__status = 'A' ).order_by('-num_visitas')

	filtrado = 5 # Show 10 contacts per page
	if 'filtrado' in request.GET:
		filtrado = request.GET.get('filtrado')
	paginator = Paginator(espacios, filtrado) # Muestra de 2 en 2
	page = request.GET.get('page')

	try:
		espacios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		espacios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		espacios = paginator.page(paginator.num_pages)

	contexto = {'espacios_recomendados':espacios_recomendados,'filtrado':filtrado,'categoria':categoria,'nuebos_socios':nuevos_socios,'socios_vip':socios_vip,'espacios':espacios,'espacios_mas_visto':espacios_mas_visto}
	return render_to_response('web/resultado.html',contexto, context_instance = RequestContext( request ))






