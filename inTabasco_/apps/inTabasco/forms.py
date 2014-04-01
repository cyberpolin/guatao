#encoding:utf-8
from django import *
from django.forms import *
from inTabasco_.apps.inTabasco.models import *
from django.forms import ModelForm
from django import forms
class regitro_socio_web_form( ModelForm ):
	red_social = forms.ModelChoiceField(required = False, label = "Red Social" , empty_label = "Seleccione la red social", queryset=cat_redes_sociales.objects.all())
	usuario_red_social = forms.CharField(required = False, label = "Usuario de la Red Social", max_length = 50)
	tipo_usuario = forms.ModelChoiceField(queryset=cat_tipo_usuario.objects.all(), initial="3", widget=forms.HiddenInput())
	fecha_nacimiento = forms.DateField(label = "Fecha de Nacimiento ", widget = forms.TextInput(attrs={'class':'datepicker'}))
	imagen = forms.ImageField(label=('Foto'),required = False)
	class Meta:
		model = cat_persona
		fields = ('imagen','nombre','apellido_paterno','apellido_materno','fecha_nacimiento','correo','telefono','celular','tipo_usuario')

	def clean(self):
		return self.cleaned_data

class contactar_socio_form( forms.Form ):
	nombre = forms.CharField( max_length = 100, widget = forms.TextInput(attrs={'placeholder':'Nombre'}) )
	correo = forms.EmailField( max_length = 100, widget = forms.TextInput(attrs={'placeholder':'Correo'}))
	asunto = forms.CharField( max_length = 100, widget = forms.TextInput(attrs={'placeholder':'Asunto'}) )
	telefono = forms.CharField( max_length = 15, widget = forms.TextInput(attrs={'placeholder':'Telefono'}) )
	comentario = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Mensaje aqui...'}))

	def clean(self):
		return self.cleaned_data
