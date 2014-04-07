from django.db import models
from django.contrib.auth.models import User
from datetime import *


class cat_status(models.Model):
    status = models.CharField(max_length=2)

    def __unicode__(self):
        return u'%s' % self.status

    class Meta:
        ordering = ['status']
        verbose_name = 'Catalogo de Status'
        verbose_name_plural = 'Catalogo de Status'
        unique_together = ['status']


class cat_tipo_usuario(models.Model):
    tipo = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % self.tipo

    class Meta:
        ordering = ['tipo']
        verbose_name = 'Catalogo de Tipos de Usuarios'
        verbose_name_plural = 'Catalogo de Tipos de Usuarios'
        unique_together = ['tipo']


class cat_persona(models.Model):
    imagen = models.ImageField(upload_to='imagenes_usuarios', blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_registro = models.DateField(default=datetime.now())
    fecha_nacimiento = models.DateField()
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    celular = models.CharField(max_length=15, blank=True, null=True)
    tipo_usuario = models.ForeignKey(cat_tipo_usuario)
    usuario = models.ForeignKey(User)
    status = models.ForeignKey( cat_status )
    agente_venta = models.ForeignKey(User, related_name = 'agente', null = True, blank = True)

    def __unicode__(self):
        return u'%s %s %s' % (self.nombre, self.apellido_paterno, self.apellido_materno)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Catalogo de Personas'
        verbose_name_plural = 'Catalogo de Personas'


class cat_promociones(models.Model):
    nombre = models.CharField(max_length=50)
    promocion = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Catalogo de Promociones'
        verbose_name_plural = 'Catalogo de Promociones'
        unique_together = ['nombre']


class cat_precios(models.Model):
    precio = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return u'%s' % self.precio

    class Meta:
        ordering = ['precio']
        verbose_name = 'Catalogo de Precios'
        verbose_name_plural = 'Catalogo de Precios'
        unique_together = ['precio']


class cat_productos(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    precio = models.ForeignKey(cat_precios)
    dias_vigente = models.IntegerField()
    promocion = models.ForeignKey(cat_promociones, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Catalogo de Productos'
        verbose_name_plural = 'Catalogo de Productos'
        unique_together = ['nombre']


class cat_localidad(models.Model):
    padre = models.ForeignKey('self', null=True, blank=True, verbose_name='pertenece a')
    nombre = models.CharField('nombre', max_length=200, help_text='Escriba el nombre', )

    def __unicode__(self):
        if self.padre == None:
            r = self.nombre
        else:
            r = u'%s - %s' % (self.padre, self.nombre)
        return u'%s' % r

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Localidades'
        verbose_name_plural = 'Localidades'
        unique_together = ['padre', 'nombre']


class cat_direcciones(models.Model):
    calle = models.CharField(max_length=30)
    numero = models.CharField(max_length=10)
    codigo_postal = models.CharField(max_length=10)
    colonia = models.CharField(max_length=30)
    localidad = models.ForeignKey(cat_localidad)
    longitud = models.CharField(max_length=300, null=True, blank=True)
    latitud = models.CharField(max_length=300, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.localidad, self.colonia, self.calle)


    class Meta:
        ordering = ['calle']
        verbose_name = 'Catalogo de Direcciones'
        verbose_name_plural = 'Catalogo de Direcciones'


class agente_ventas(models.Model):
    padre = models.ForeignKey('self', null=True, blank=True, verbose_name='Pertenece a')
    nombre = models.ForeignKey(cat_persona)
    direccion = models.ForeignKey(cat_direcciones)
    usuario = models.ForeignKey(User)
    status = models.ForeignKey(cat_status)

    def __unicode__(self):
        if self.padre == None:
            r = self.nombre
        else:
            r = u'%s - %s' % (self.padre, self.nombre)
        return u'%s' % r

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Agente de Ventas'
        verbose_name_plural = 'Agente de Ventas'
        unique_together = ['nombre']
        permissions = (
            ('consulta_agente', 'Consultar a los agentes'),
            ('corte_agente', 'Corte a los agentes'),
            ('corte_general_agente', 'Corte general los agentes'),
        )


class cat_categorias_espacios(models.Model):
    clave = models.CharField(max_length=4)
    categoria = models.CharField(max_length=50)
    icono = models.ImageField(upload_to='imagenes_usuarios', blank=True, null=True)

    def __unicode__(self):
        return u' %s ' % self.categoria

    class Meta:
        ordering = ['categoria']
        verbose_name = 'catalogo de categoria'
        verbose_name_plural = 'Catalogo de Categorias para Espacios'
        unique_together = ['clave', 'categoria']


class espacio(models.Model):
    rfc = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    propietario = models.ForeignKey(cat_persona)
    descripcion_corta = models.CharField(max_length=250)
    descripcion_larga = models.TextField(max_length=None)
    categorias = models.ManyToManyField( cat_categorias_espacios )
    direccion = models.ForeignKey(cat_direcciones)
    url = models.URLField(max_length=150, blank=True, null=True)
    socio_vip = models.BooleanField( default=False )
    dias_laborales = models.CharField( max_length=500 )
    horario_atencion = models.CharField( max_length=100 )
    num_visitas = models.IntegerField(default=0)
    usuario = models.ForeignKey(User)
    status = models.ForeignKey(cat_status)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Espacios'
        verbose_name_plural = 'Espacios'
        permissions = (
            ('consulta_espacio', 'Consultar a los espacios'),
        )


class cat_redes_sociales(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    reglas = models.CharField(max_length=300)

    def __unicode__(self):
        return u'%s' % self.nombre


    class Meta:
        ordering = ['nombre']
        verbose_name = 'Catalogo de Redes Sociales'
        verbose_name_plural = 'Catalogo de Redes Sociales'


class usr_redes_sociales(models.Model):
    usuario = models.ForeignKey(cat_persona)
    red_social = models.ForeignKey(cat_redes_sociales)
    nombre_red = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.nombre_red


    class Meta:
        ordering = ['nombre_red']
        verbose_name = 'Usuarios de Redes Sociales'
        verbose_name_plural = 'Usuarios de Redes Sociales'
        unique_together = ['nombre_red']


class cat_imagenes(models.Model):
    imagen = models.ImageField(upload_to='imagenes_usuarios')  #investigar el uso de carpetas dinamicas
    espacio = models.ForeignKey(espacio)

    def __unicode__(self):
        return u'%s' % self.imagen

    class Meta:
        ordering = ['espacio']
        verbose_name = 'Catalogo de Imagenes'
        verbose_name_plural = 'Catalogo de Imagenes'


class venta(models.Model):
    agente = models.ForeignKey(User)
    fecha_venta = models.DateField(default=datetime.now())
    propietario = models.ForeignKey(cat_persona)
    espacio = models.ForeignKey(espacio)
    producto = models.ForeignKey(cat_productos)

    def __unicode__(self):
        return u'%s' % self.espacio

    def _get_importe(self):
        return self.producto.precio.precio * int(3)

    importe = property(_get_importe)

    class Meta:
        verbose_name = 'Ventas'
        verbose_name_plural = 'Ventas'
        permissions = (
            ('consulta_venta', 'Consultar a los las ventas del dia'),
        )


class cat_tipo_movimiento(models.Model):
    movimiento = models.CharField(max_length=100)
    accion = models.BooleanField()

    def __unicode__(self):
        return u'%s' % self.movimiento

    class Meta:
        ordering = ['movimiento']
        verbose_name = 'Catalogo de Movimientos'
        verbose_name_plural = 'Catalogo de Movimientos'
        unique_together = ['movimiento']


class caja(models.Model):
    movimiento = models.ForeignKey(cat_tipo_movimiento)
    descripcion = models.CharField(max_length=300)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    fecha = models.DateField(default=datetime.now())

    def __unicode__(self):
        return u'%s' % self.movimiento.movimiento + ' - ' + u'%s' % self.descripcion

    class Meta:
        ordering = ['movimiento']
        verbose_name = 'Caja'
        verbose_name_plural = 'Caja'
        permissions = (
            ('consulta_caja', 'Consultar el saldo en caja'),
        )


class recomendaciones( models.Model ):
    nombre_usuario = models.CharField( max_length = 150 )
    fecha = models.DateTimeField( auto_now = True)
    opinion = models.TextField()
    calificacion = models.IntegerField()
    espacio = models.ForeignKey(espacio)

    def __unicode__(self):
        return u'%s' % self.nombre_usuario

    class Meta:
        ordering = ['nombre_usuario','fecha']
        verbose_name = 'recomendaciones'
        verbose_name_plural = 'Recomiendame'

class contactame( models.Model ):
    nombre = models.CharField( max_length = 100 )
    correo = models.EmailField( max_length = 100)
    asunto = models.CharField( max_length = 100 )
    telefono = models.CharField( max_length = 15 )
    comentario = models.TextField()
    fecha_mensaje = models.DateField( default = datetime.now() )
    socio_contactar = models.ForeignKey( cat_persona )
    leido = models.BooleanField( default = False )

    def __unicode__(self):
        return u'%s' % self.asunto

    class Meta:
        ordering = ['fecha_mensaje']
        verbose_name = 'contactame'
        verbose_name_plural = 'Contactame'







