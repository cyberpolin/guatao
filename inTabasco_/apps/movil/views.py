#encoding:utf-8
from django.http import *
from django.contrib.auth.decorators import * # Libreria para el login required
from django.shortcuts import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from inTabasco_.apps.movil.forms import *
from django.contrib import messages
from inTabasco_.apps.inTabasco.forms import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt


#Carlos Vasconcelos

from django.shortcuts import render_to_response, redirect
from inTabasco_.apps.inTabasco.models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import string, random


@login_required(login_url='/movil/login/')
def index(request):
        personaId = cat_persona.objects.get(usuario_id = request.user.pk)
        socios = cat_persona.objects.filter(agente_venta_id =personaId.usuario_id)
        socios = dict(socios = socios)
        return render_to_response('movil/index.html', socios)

def loginView(request):
    if request.user.is_authenticated():
        return redirect('index')

    if (request.POST):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                persona = cat_persona.objects.get( usuario = user)
                if (persona.tipo_usuario.tipo =='Agente'):
                    return redirect('index')
                else:
                    mensaje = mensaje + 'Cuenta desactivada'
        else:
            request.mensaje = 'El usuario o contraseña son incorrectas.'
            #request.POST = None
            return redirect('loginView')
    else:
        return render_to_response('movil/login.html', context_instance=RequestContext(request))

    return render_to_response('movil/addSocio.html', contexto, context_instance = RequestContext(request))

@login_required(login_url='/movil/login/')
@permission_required('inTabasco.add_espacio', raise_exception=True)
def nuevo_socio(request,pk):
    formulario_espacio_socio = Registrar_Espacio_Socio()
    list_socios = cat_persona.objects.filter( tipo_usuario__tipo = 'Socio')
    socios = list_socios.count()
    contexto = {'alta_espacio':'active',
                'request':request,
                'list_socios':list_socios,
                'socios':socios,
                'formulario_espacio_socio':formulario_espacio_socio}
    if pk == '0':
        print ('entro')
        formulario_persona_espacio_socio = Registrar_Persona_Socio()
        formulario_socio = UserCreationForm()
        contexto['formulario_socio'] = formulario_socio
        contexto['formulario_persona_espacio_socio']=formulario_persona_espacio_socio

    #Si tiene POST
    if request.POST:
        if pk != '0':
            if formulario_espacio_socio.is_valid():
                return redirect('index')
            else:
                formulario_espacio_socio = Registrar_Espacio_Socio(request.POST, request.FILES)
                contexto = {'alta_espacio':'active',
                    'request':request,'list_socios':list_socios,
                    #'socios':socios,'formulario_socio':formulario_socio,
                    #'formulario_persona_espacio_socio':formulario_persona_espacio_socio,
                    'formulario_espacio_socio':formulario_espacio_socio}
                return render_to_response('movil/addSocio.html', contexto, context_instance = RequestContext(request))


        else:
            if formulario_socio.is_valid() and formulario_persona_espacio_socio.is_valid() and formulario_espacio_socio.is_valid():
                #Variable datos de formulario
                foto = formulario_persona_espacio_socio.cleaned_data['foto']
                nombre_propietario = formulario_persona_espacio_socio.cleaned_data['nombre_propietario']
                apellido_paterno = formulario_persona_espacio_socio.cleaned_data['apellido_paterno']
                apellido_materno = formulario_persona_espacio_socio.cleaned_data['apellido_materno']
                fecha_nacimiento = formulario_persona_espacio_socio.cleaned_data['fecha_nacimiento']
                correo = formulario_persona_espacio_socio.cleaned_data['correo']
                telefono = formulario_persona_espacio_socio.cleaned_data['telefono']
                celular = formulario_persona_espacio_socio.cleaned_data['celular']
                tipo_usuario = cat_tipo_usuario.objects.get(pk = 3)


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
                persona.tipo_usuario = tipo_usuario
                persona.usuario = usuario_
                persona.agente_venta = request.user
                persona.status_id = 1
                persona.save()

                #####
                localidad = formulario_espacio_socio.cleaned_data['localidad']
                colonia = formulario_espacio_socio.cleaned_data['colonia']
                calle = formulario_espacio_socio.cleaned_data['calle']
                numero = formulario_espacio_socio.cleaned_data['numero']
                codigo_postal = formulario_espacio_socio.cleaned_data['codigo_postal']
                dias_laborales = formulario_espacio_socio.cleaned_data['dias_laborales']
                horario_atencion = formulario_espacio_socio.cleaned_data['horario_atencion']
                latitud = formulario_espacio_socio.cleaned_data['latitud']
                longitud = formulario_espacio_socio.cleaned_data['longitud']

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
                rfc = formulario_espacio_socio.cleaned_data['rfc']
                nombre_establecimiento = formulario_espacio_socio.cleaned_data['nombre_establecimiento']
                descripcion_corta = formulario_espacio_socio.cleaned_data['descripcion_corta']
                descripcion_larga = formulario_espacio_socio.cleaned_data['descripcion_larga']
                url = formulario_espacio_socio.cleaned_data['url']
                socio_vip = formulario_espacio_socio.cleaned_data['socio_vip']
                #status = formulario_espacio_socio.cleaned_data['status']
                persona2 = cat_persona.objects.get(pk = persona.pk)
                espacio_socio = espacio()
                espacio_socio.rfc = rfc
                espacio_socio.nombre = nombre_establecimiento
                espacio_socio.propietario = persona2
                espacio_socio.descripcion_corta = descripcion_corta
                espacio_socio.descripcion_larga = descripcion_larga
                espacio_socio.direccion = direccion
                espacio_socio.url = url
                espacio_socio.socio_vip = socio_vip
                espacio_socio.dias_laborales = dias_laborales
                espacio_socio.horario_atencion = horario_atencion
                espacio_socio.usuario = request.user
                espacio_socio.status = cat_status.objects.get(pk = 1)
                espacio_socio.producto = cat_productos.objects.get(pk = 1)
                espacio_socio.save()
                categorias = request.POST.getlist( 'categorias' )

                for p in categorias:
                    espacio_socio.categorias.add(p)
                    espacio_socio.save()

                #Agrega la imagen del negocio ala tabla Cat_imagenes#
                imagen = formulario_espacio_socio.cleaned_data['imagen']
                imagen_espacio = cat_imagenes(imagen = imagen,
                                                espacio = espacio_socio)
                imagen_espacio.save()

                #Se guarda la tabla de venta#
                producto = request.POST.get('producto')
                consulta_producto = cat_productos.objects.all().get(id = 1)

                ventas = venta(agente = request.user,
                                fecha_venta = datetime.now(),
                                espacio = espacio_socio,
                                )
                ventas.save()

                return redirect('index')
            else:
                formulario_espacio_socio = Registrar_Espacio_Socio(request.POST, request.FILES)
                contexto = {'alta_espacio':'active',
                    'request':request,'list_socios':list_socios,
                    'socios':socios,'formulario_socio':formulario_socio,
                    'formulario_persona_espacio_socio':formulario_persona_espacio_socio,
                    'formulario_espacio_socio':formulario_espacio_socio}

                if pk == '0':
                    print 'pk 0'
                    formulario_persona_espacio_socio = Registrar_Persona_Socio(request.POST, request.FILES)
                    formulario_socio = UserCreationForm(request.POST)
                    contexto['formulario_persona_espacio_socio']=formulario_persona_espacio_socio,
                    contexto['formulario_socio'] = formulario_socio
                return render_to_response('movil/addSocio.html', contexto, context_instance = RequestContext(request))

    #De lo Contrario tiene POST
    else:
        print 'normal'
        return render_to_response('movil/addSocio.html', contexto, context_instance = RequestContext(request))

#Listar espacios por socio

def lista_espacios(request, pk):
    espacios = espacio.objects.filter(propietario = pk)
    espacios = dict( espacios = espacios )
    return render_to_response('movil/index.html', espacios)

def reset_pasword(request, pk):
    base=string.ascii + string.digits
    password = ''.join(random.choice(base) for _ in range(8))
    usuario = cat_persona.objects.get(pk= pk).usuario_id
    socio = User.objects.get(pk=usuario)
    socio.set_password(password)
    socio.save()
    titulo= 'Tu nueva contraseña.'
    mensaje = 'Estimado '+ socio.first_name + ' ' + socio.last_name + ', te enviamos tu nueva contrasena, por favor cuando accedas a tu panel de administracion cambiala por una que recuerdes.\n En guatao.mx es muy importante que puedas acceder a tu cuenta, es por eso que estamos a tu orden cuando lo necesites.\n Tu nueva contrasena es '+ password + '     y puedes acceder a tu panel de control en http://guatao.mx/admin/'
    correo = socio.email
    send_mail(titulo, mensaje, 'info@guatao.mx',[correo], fail_silently=False)
    return redirect('lista_espacios', pk)