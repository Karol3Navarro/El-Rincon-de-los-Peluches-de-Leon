from django.shortcuts import render, get_object_or_404
from admin_peluches.models import Categoria, Peluche, Configuracion
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    peluches = Peluche.objects.filter(estado_revision__in=['Publicado', 'Vendido'])
    categorias = Categoria.objects.all()
    context= {'peluches': peluches, 'categorias': categorias}
    return render(request, 'peluches/index.html', context)

def peluches(request):
    peluches = Peluche.objects.filter(estado_revision__in=['Publicado', 'Vendido'])

    # Obtener filtros desde GET
    # categoria_id = request.GET.get('categoria')
    categorias_ids = request.GET.getlist('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    query = request.GET.get('q')

    estados = request.GET.getlist('estado')
    tamanos = request.GET.getlist('tamano')
    min_cm = request.GET.get('min_cm')
    max_cm = request.GET.get('max_cm')

    #Categoria
    if categorias_ids:
        peluches = peluches.filter(categoria_id__in=categorias_ids)

    #Precio
    if precio_min and precio_min != "":
        precio_min_val = int(precio_min.replace(".", ""))
        peluches = peluches.filter(precio__gte=precio_min_val)

    if precio_max and precio_max != "":
        precio_max_val = int(precio_max.replace(".", ""))
        peluches = peluches.filter(precio__lte=precio_max_val)

    #Estado
    if estados:
        peluches = peluches.filter(estado_revision__in=estados)
    # TAMAÑO
    if tamanos:
        peluches = peluches.filter(tamano__in=tamanos)

    # ALTURA (CM)
    try:
        if min_cm:
            min_cm = int(min_cm)
            peluches = peluches.filter(alto_cm__gte=min_cm)

        if max_cm:
            max_cm = int(max_cm)
            peluches = peluches.filter(alto_cm__lte=max_cm)
    except ValueError:
        pass
    
    #Filtrar por búsqueda
    if query and query.strip() != "":  
        peluches = peluches.filter(
            Q(nombre__icontains=query) | Q(categoria__categoria__icontains=query)
        )

    categorias = Categoria.objects.all()
    # 🔥 PAGINACIÓN
    paginator = Paginator(peluches, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'peluches': page_obj,
        'page_obj': page_obj,
        'categorias': categorias,
        'filtro_categoria': categorias_ids,
        'filtro_precio_min': precio_min,
        'filtro_precio_max': precio_max,
        'estado_seleccionado': estados,
        'tamanos': Peluche.TAMANOS,
        'tamano_seleccionado': tamanos,
        'min_cm': min_cm or '',
        'max_cm': max_cm or '',
        'query': query,
    }
    return render(request, 'peluches/peluches.html', context)

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
    categorias = Categoria.objects.all()

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
        'categorias':categorias,
        'imagen_url': imagen_url,
        'producto_url': producto_url,
        'mensaje': mensaje,
        'telefono_whatsapp': telefono_whatsapp,
        'peluches_relacionados': peluches_relacionados,
    }
    return render(request, 'peluches/ver_peluche.html', context)