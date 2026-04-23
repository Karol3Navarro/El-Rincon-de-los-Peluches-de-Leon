from admin_peluches.models import Configuracion

def config_global(request):
    configuracion = Configuracion.objects.first()

    return {
        'telefono_whatsapp': configuracion.telefono_whatsapp if configuracion else "56900000000"
    }