from inTabasco_.apps.inTabasco.models import *
from django.contrib import admin


class PersonAdmin(admin.ModelAdmin):
    list_filter = ('tipo_usuario', 'nombre', 'apellido_paterno', 'fecha_registro')
    list_display = ('nombre', 'apellido_paterno', 'fecha_registro', 'tipo_usuario')
    #search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'fecha_registro', 'tipo_usuario')

admin.site.register( cat_persona, PersonAdmin )
admin.site.register( cat_promociones )
admin.site.register( cat_precios )
admin.site.register( cat_productos )
admin.site.register( cat_localidad )
admin.site.register( cat_direcciones )
admin.site.register( agente_ventas )
admin.site.register( cat_categorias_espacios )
admin.site.register( espacio )
admin.site.register( cat_redes_sociales )
admin.site.register( cat_imagenes )
admin.site.register( venta )
admin.site.register( cat_status )
admin.site.register( cat_tipo_movimiento )
admin.site.register( caja )
admin.site.register( cat_tipo_usuario )
admin.site.register( recomendaciones )
admin.site.register( contactame )