from django.shortcuts import render, get_object_or_404
from admin_peluches.models import Categoria, Peluche, Configuracion

# Create your views here.

def index(request):
    peluches = Peluche.objects.filter(estado_revision__in=['Publicado', 'Vendido'])
    context= {'peluches': peluches}
    return render(request, 'peluches/index.html', context)

def peluches(request):
    peluches = Peluche.objects.filter(estado_revision='Publicado')

    # Obtener filtros desde GET
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')

    if categoria_id and categoria_id != "":
        peluches = peluches.filter(categoria_id=categoria_id)

    if precio_min and precio_min != "":
        # Convertimos a número eliminando puntos si existieran
        precio_min_val = int(precio_min.replace(".", ""))
        peluches = peluches.filter(precio__gte=precio_min_val)

    if precio_max and precio_max != "":
        precio_max_val = int(precio_max.replace(".", ""))
        peluches = peluches.filter(precio__lte=precio_max_val)

    categorias = Categoria.objects.all()

    context = {
        'peluches': peluches,
        'categorias': categorias,
        'filtro_categoria': categoria_id,
        'filtro_precio_min': precio_min,
        'filtro_precio_max': precio_max,
    }
    return render(request, 'peluches/peluches.html', context)


# def peluches(request):
#     peluches_qs = Peluche.objects.filter(estado_revision='Publicado')

#     # Obtener filtros desde GET
#     categoria_id = request.GET.get('categoria', '')
#     precio_min = request.GET.get('precio_min', '')
#     precio_max = request.GET.get('precio_max', '')

#     # Filtrar por categoría primero
#     if categoria_id:
#         peluches_qs = peluches_qs.filter(categoria_id=categoria_id)

#     # Filtrar por precio en Python
#     peluches = []
#     for p in peluches_qs:
#         try:
#             precio_num = int(p.precio.replace(".", "")) if p.precio else 0
#         except ValueError:
#             precio_num = 0

#         if precio_min:
#             try:
#                 min_val = int(precio_min.replace(".", ""))
#                 if precio_num < min_val:
#                     continue
#             except ValueError:
#                 pass

#         if precio_max:
#             try:
#                 max_val = int(precio_max.replace(".", ""))
#                 if precio_num > max_val:
#                     continue
#             except ValueError:
#                 pass

#         peluches.append(p)

#     categorias = Categoria.objects.all()

#     context = {
#         'peluches': peluches,
#         'categorias': categorias,
#         'filtro_categoria': categoria_id,
#         'filtro_precio_min': precio_min,
#         'filtro_precio_max': precio_max,
#     }
#     return render(request, 'peluches/peluches.html', context)

def peluches_vendidos(request):
    peluches = Peluche.objects.filter(estado_revision='Vendido')
    context= {'peluches': peluches}
    return render(request, 'peluches/peluches_vendidos.html', context)

#Aun no se puede ver la imagen en Whatsapp
#Chatgpt dice probar con ngrok
#o Render, Railway pero hay que subirlo a github

#ESTE ES CON EL NUMERO DENTRO DEL HTML
# def ver_peluche(request, id_peluche):
#     peluche = get_object_or_404(Peluche, id_peluche=id_peluche)

#     # Obtener primera imagen
#     imagen_url = ""
#     if peluche.imagenes.exists():
#         imagen_url = request.build_absolute_uri(
#             peluche.imagenes.first().imagen.url
#         )

#     # URL del producto (para compartir)
#     producto_url = request.build_absolute_uri(request.path)

#     # Mensaje WhatsApp
#     mensaje = f"Hola, me interesa este peluche {peluche.nombre} {producto_url}"

#     context = {'peluche': peluche, 'imagen_url': imagen_url, 'producto_url': producto_url, 'mensaje': mensaje}
#     return render(request, 'peluches/ver_peluche.html', context)

def ver_peluche(request, id_peluche):
    peluche = get_object_or_404(Peluche, id_peluche=id_peluche)

    imagen_url = ""
    if peluche.imagenes.exists():
        imagen_url = request.build_absolute_uri(peluche.imagenes.first().imagen.url)

    producto_url = request.build_absolute_uri(request.path)

    # Tomamos la configuración del admin (solo la primera)
    configuracion = Configuracion.objects.first()
    telefono_whatsapp = configuracion.telefono_whatsapp if configuracion else "56900000000"

    mensaje = f"Hola, me interesa este peluche 🧸 {peluche.nombre} {producto_url}"

    # Peluches relacionados (misma categoría, distintos del peluche actual)
    peluches_relacionados = Peluche.objects.filter(categoria=peluche.categoria).exclude(id_peluche=peluche.id_peluche)[:4]

    context = {
        'peluche': peluche,
        'imagen_url': imagen_url,
        'producto_url': producto_url,
        'mensaje': mensaje,
        'telefono_whatsapp': telefono_whatsapp,
        'peluches_relacionados': peluches_relacionados,
    }
    return render(request, 'peluches/ver_peluche.html', context)