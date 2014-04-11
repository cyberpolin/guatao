#encoding:utf-8
from django import *
from django.forms import *
from inTabasco_.apps.inTabasco.models import *
from django import forms
from django.db.models import Q
from django.forms import ModelForm

class Registrar_Agente( forms.Form ):
    padre = forms.ModelChoiceField(required =False, empty_label = 'Seleccione su Agente Padre', queryset = cat_persona.objects.filter(tipo_usuario__tipo = 'Agente'), widget = forms.Select(attrs={'class':'chzn-select'}))
    foto = forms.ImageField( required = False )
    nombre = forms.CharField(label="Nombre", max_length = 50 )
    apellido_paterno = forms.CharField(label="Apellido Paterno", max_length = 50 )
    apellido_materno = forms.CharField(label="Apellido Materno", max_length = 50 )
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget = forms.TextInput(attrs={'class':'datepicker'}))
    correo = forms.EmailField(label = "Correo", max_length=100)
    telefono = forms.CharField(label="Teléfono", max_length=15)
    celular = forms.CharField(max_length=15, required=False)
    localidad = forms.ModelChoiceField(empty_label = "Seleccione la localidad",queryset=cat_localidad.objects.all().exclude(padre_id =  None), widget = forms.Select(attrs={'class':'chzn-select'}))
    colonia = forms.CharField(label = "Colonia", max_length = "30" )
    calle = forms.CharField(label = "Calle", max_length = "30")
    numero = forms.CharField(label = "Numero", max_length = "10")
    codigo_postal = forms.CharField(label="Codigo Postal", max_length = "10")

    latitud = forms.CharField(widget = forms.HiddenInput(), initial="18.000264246324", label="Latitud", max_length = "300")
    longitud = forms.CharField(widget = forms.HiddenInput(), initial="-92.94361710548401", label="Longitud", max_length = "300")
    status = forms.ModelChoiceField(initial="1", queryset=cat_status.objects.all(), widget = forms.Select(attrs={'style':'display:none'}))
    tipo_usuario = forms.ModelChoiceField(initial="2", queryset=cat_tipo_usuario.objects.all(), widget = forms.Select(attrs={'style':'display:none'}))


class Registrar_Persona_Socio( forms.Form):
    foto = forms.ImageField(required = False)
    nombre_propietario = forms.CharField(label = "Nombre del Propietario: ", max_length = 50)
    apellido_paterno = forms.CharField(label = "Apellido Paterno ", max_length = 50)
    apellido_materno = forms.CharField(label = "Apellido Materno ", max_length = 50)
    fecha_nacimiento = forms.DateField(label = "Fecha de Nacimiento ", widget = forms.TextInput(attrs={'class':'datepicker'}))
    correo = forms.EmailField(label = "Correo Electronico", max_length = 100)
    telefono = forms.CharField(label = "Telefono", max_length = 15)
    celular = forms.CharField(label = "Celular", max_length = 15)
    red_social = forms.ModelChoiceField(required = False, label = "Red Social" , empty_label = "Seleccione la red social", queryset=cat_redes_sociales.objects.all())
    usuario_red_social = forms.CharField(required = False, label = "Usuario de la Red Social", max_length = 50)

    tipo_usuario = forms.ModelChoiceField(queryset=cat_tipo_usuario.objects.all(), initial="3", widget=forms.HiddenInput())

class Registrar_Espacio_Socio( forms.Form):
    imagen = forms.ImageField(label = "Imagen del Establecimiento", required = False)
    rfc = forms.CharField(label = "RFC del Establecimiento", max_length = "20", required = False)
    nombre_establecimiento = forms.CharField(label = "Nombre del Establecimiento ", max_length = 200)


    descripcion_corta = forms.CharField(label = "Descripcion Corta del Establecimiento", max_length = 250 )
    descripcion_larga = forms.CharField(widget=forms.Textarea(attrs={'class':'input-xlarge textarea','style':'width: 330px; height: 200px'}), label = "Descripcion Larga del Establecimiento" )
    categorias = forms.ModelMultipleChoiceField(queryset=cat_categorias_espacios.objects.all(), widget=forms.CheckboxSelectMultiple)
    socio_vip = forms.BooleanField(initial=False, required=False)
    localidad = forms.ModelChoiceField(empty_label = "Seleccione la localidad",queryset=cat_localidad.objects.all().exclude(padre_id =  None), widget = forms.Select(attrs={'class':'chzn-select'}))
    colonia = forms.CharField(label = "Colonia", max_length = "30" )
    calle = forms.CharField(label = "Calle", max_length = "30")
    numero = forms.CharField(label = "Numero", max_length = "10")
    codigo_postal = forms.CharField(label="Codigo Postal", max_length = "10")
    dias_laborales = forms.CharField(label="Dias de Atencion", max_length = "500")
    horario_atencion = forms.CharField(label="Horario de Atencion", max_length = "100")
    latitud = forms.CharField(initial="18.000264246324", label="Latitud", max_length = "300", widget = forms.HiddenInput())
    longitud = forms.CharField(initial="-92.94361710548401", label="Longitud", max_length = "300", widget = forms.HiddenInput())

    url = forms.URLField(label ='Pagina Web', max_length = 150, required = False)
    producto = forms.ModelChoiceField(  empty_label = "Seleccione el producto", queryset=cat_productos.objects.all(), widget = forms.Select(attrs={'class':'chzn-select'}))
    status = forms.ModelChoiceField(queryset=cat_status.objects.all(), initial='1', widget = forms.HiddenInput())

