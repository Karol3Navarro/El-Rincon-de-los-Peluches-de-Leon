from django.shortcuts import render, get_object_or_404
from admin_peluches.models import Categoria, Peluche, Configuracion
from django.db.models import Q, Count
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    peluches = (
        Peluche.objects
        .filter(estado_revision__in=['Publicado', 'Vendido'])
        .order_by('-id_peluche')[:20]
    )
    categorias = Categoria.objects.all()
    context= {'peluches': peluches, 'categorias': categorias}
    return render(request, 'peluches/index.html', context)

def peluches(request):
    peluches = Peluche.objects.filter(estado_revision__in=['Publicado', 'Vendido']).order_by('-id_peluche')

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
    # if query and query.strip():
    #     words = query.split()

    #     q = Q()

    #     for word in words:
    #         q |= (
    #             Q(nombre__iregex=r'\b' + word + r'\b') |
    #             Q(descripcion__iregex=r'\b' + word + r'\b') |
    #             Q(categoria__categoria__iregex=r'\b' + word + r'\b') |
    #             Q(tamano__iregex=r'\b' + word + r'\b') |
    #             Q(estado_revision__iregex=r'\b' + word + r'\b')
    #         )

    #     peluches = peluches.filter(q).distinct()
    if query and query.strip():
        words = query.split()

        for word in words:
            peluches = peluches.filter(
                Q(nombre__icontains=word) |
                Q(descripcion__icontains=word) |
                Q(categoria__categoria__icontains=word) |
                Q(tamano__icontains=word) |
                Q(estado_revision__icontains=word)
            ).distinct()
    categorias = (
        Categoria.objects
        .annotate(
            total_peluches=Count(
                'peluche',
                filter=Q(peluche__estado_revision__in=['Publicado', 'Vendido'])
            )
        )
    )
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

def ver_peluche(request, id_peluche, nombre):
    peluche = get_object_or_404(Peluche, id_peluche=id_peluche)
    categorias = Categoria.objects.all()

    imagen_url = ""
    if peluche.imagenes.exists():
        imagen_url = request.build_absolute_uri(peluche.imagenes.first().imagen.url)

    producto_url = request.build_absolute_uri(request.path)

    configuracion = Configuracion.objects.first()
    telefono_whatsapp = configuracion.telefono_whatsapp if configuracion else "56900000000"

    mensaje = (
        f"Hola, me interesa este peluche\n"
        f"*Nombre:* {peluche.nombre}\n"
        f"{producto_url}"
    )

    # Peluches relacionados (misma categoría, distintos del peluche actual)
    peluches_relacionados = (
        Peluche.objects
        .filter(categoria=peluche.categoria)
        .exclude(id_peluche=peluche.id_peluche)
        .exclude(estado_revision__in=['Vendido', 'Sin Publicar'])
        .order_by('?')[:4]
    )

    # Completar hasta 4 si faltan
    faltantes = 4 - peluches_relacionados.count()

    if faltantes > 0:
        ids_existentes = peluches_relacionados.values_list('id_peluche', flat=True)

        adicionales = (
            Peluche.objects
            .exclude(id_peluche__in=ids_existentes)
            .exclude(id_peluche=peluche.id_peluche)
            .exclude(estado_revision__in=['Vendido', 'Sin Publicar'])
            .order_by('?')[:faltantes]
        )

        peluches_relacionados = peluches_relacionados | adicionales

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