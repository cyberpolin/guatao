#encoding:utf-8
from django import *
from django.forms import *
from inTabasco_.apps.inTabasco.models import *
from django import forms
from django.db.models import Q
from django.forms import ModelForm

class Registrar_Persona_Socio( forms.Form):
    foto = forms.ImageField(label = "Fotografia del Socio", required = False, widget = forms.FileInput(attrs={'class':'upload'})) #accept="image/*" capture="camera"
    nombre_propietario = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellido_paterno = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}))
    apellido_materno = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno'}))
    fecha_nacimiento = forms.DateField(label = " Fecha de Nac. ", widget=forms.TextInput(attrs={'placeholder': 'Fecha de nac. (dd/mm/aa)', 'type': 'date'}))
    correo = forms.EmailField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Correo Electronico'}))
    telefono = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Telefono'}))
    celular = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Celular'}))

class Registrar_Espacio_Socio( forms.Form):
    imagen = forms.ImageField(label = "Imagen del Negocio",widget = forms.FileInput(attrs={'class':'upload'}))
    rfc = forms.CharField(label = "", required = False, widget=forms.TextInput(attrs={'placeholder': 'RFC (No requerido'}))
    nombre_establecimiento = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Nombre del Negocio'}))
    descripcion_corta = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Descripción Corta'}))
    descripcion_larga = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Descripción larga del negocio'}))
    categorias = forms.ModelMultipleChoiceField(queryset=cat_categorias_espacios.objects.all())
    socio_vip = forms.BooleanField(initial=False, required=False)
    localidad = forms.ModelChoiceField(empty_label = "Seleccione la localidad",queryset=cat_localidad.objects.all().exclude(padre_id =  None), widget = forms.Select(attrs={'class':'chzn-select'}))
    colonia = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Colonia'}))
    calle = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Calle'}))
    numero = forms.CharField(label = "",widget=forms.TextInput(attrs={'placeholder': 'Numero'}))
    codigo_postal = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Codigo Postal'}))
    dias_laborales = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Lunes - Viernes'}))
    horario_atencion = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': '9:00am - 8:00pm'}))
    latitud = forms.CharField(initial=17.987557,widget=forms.HiddenInput())
    longitud = forms.CharField(initial="-92.929147",widget=forms.HiddenInput())
    url = forms.URLField(label = "", required = False, widget=forms.TextInput(attrs={'placeholder': 'URL...'}))