from django.contrib import admin
from .models import Categoria, Peluche, PelucheImagen, Configuracion

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Peluche)
admin.site.register(PelucheImagen)

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('telefono_whatsapp',)