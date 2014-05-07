#encoding:utf-8
from django.http import *
from django.contrib.auth import * 
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError

from django.contrib.auth.decorators import *
from django.contrib import messages

def reset_password(request):
    correo = request.POST.get('email')    
    consulta_user = User.objects.all().filter(email=correo)
    new_password = User.objects.make_random_password(length=10)
    idi=0
    name=""
    password=""
    email=""
    for p in consulta_user:
        idi=p.id
        name = p.username
        password=p.password
        email=p.email

    
    #return HttpResponse(usuario)
    try:
        usuario = User.objects.all().get(pk=idi)    
    except User.DoesNotExist:
        
        msj='El correo no existe, o Verifique que lo escribio correctamente' 
        messages.success(request, msj)        
        return HttpResponseRedirect('/')
        raise Http404   
    usuario.set_password(new_password)
    usuario.save()  
    #return HttpResponse(new_password)
    msj = str('Su nueva contrasena es: '+new_password+ '. Por su seguridad se recomienda cambiarla.')
    #return HttpResponse(msj)
    subject = request.POST.get('subject', 'Contraseña Nueva')
    message = request.POST.get('message', msj)
    from_email = request.POST.get('from_email', 'jonatansimpleplan89@gmail.com')
    var_email=str(email)
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [var_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        msj='Un correo se a enviado a su bandeja con su nueva contraseña' 
        messages.success(request, msj)
        return HttpResponseRedirect('/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
