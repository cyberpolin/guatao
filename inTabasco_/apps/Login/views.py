#encoding:utf-8
from django.http import *
from django.shortcuts import * #Libreria para el HttpResponse
from django.template.response import *

from django.contrib.auth import * # Libreria para validar
from django.contrib.auth.decorators import * # Libreria para el login_required

from django.contrib.auth.decorators import *
from django.contrib import messages
from inTabasco_.apps.inTabasco.models import *

def login_(request):
    return HttpResponseRedirect('/')

def validar(request):
    username = request.POST['user_login']
    password = request.POST['user_pass']
    user = authenticate(username=username, password=password)
    mensaje = ''
    if user is not None:
        if user.is_active:
            login(request, user)
            persona = cat_persona.objects.get( usuario = user)
            if (persona.tipo_usuario.tipo =='Administradores') or (persona.tipo_usuario.tipo =='Agente'):
                msj='Bienvenido ' + str(user) + ' a guatao.com.mx'
                messages.success(request, msj)
                return HttpResponseRedirect( '/principal/' )
            elif(persona.tipo_usuario.tipo =='Socio'):
                login(request, user)
                msj='Bienvenido ' + str(user) + ' a guatao.com.mx'
                messages.success(request, msj)
                return HttpResponseRedirect( '/' )
        else:
            mensaje = 'Cuenta desactivada comuniquese con el administrador.'
            messages.success(request, mensaje)
            return HttpResponseRedirect('/')

    else:
        mensaje = 'El usuario o contraseña son incorrectas.'
        messages.success(request, mensaje)
        return HttpResponseRedirect('/')

@login_required(login_url='/login_')
def logout_user(request):
    response = logout(request)
    return HttpResponseRedirect('/')

